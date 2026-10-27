"""OmniVoice adapter against a fake Gradio server: contract, errors, validation."""
import shutil
import tempfile
import unittest
from pathlib import Path

from integrations import audio_probe
from integrations.tts import omnivoice as ov
from tests.fake_omnivoice import FakeOmniVoice, unused_port

HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
TEXT = "Hello there friend, this is a test."  # 7 words in a 2 s fake clip = 3.5 words/s
DESIGN = ov.VoiceSpec(mode="design", design={"gender": "Male", "accent": "British Accent"})


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg/ffprobe required")
class AdapterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "out.wav"

    def tearDown(self):
        self.tmp.cleanup()

    def client(self, fake, **kw):
        return ov.OmniVoiceClient(base_url=fake.url, retries=0, model_revision="test", **kw)

    def test_connection_error_is_clear(self):
        client = ov.OmniVoiceClient(base_url=f"http://127.0.0.1:{unused_port()}", retries=1, model_revision="t")
        with self.assertRaisesRegex(ov.OmniVoiceUnavailable, "not reachable.*omnivoice-demo"):
            client.health()

    def test_health_and_voice_options_come_from_live_contract(self):
        with FakeOmniVoice() as fake:
            h = self.client(fake).health()
            self.assertTrue(h["english_supported"])
            self.assertEqual(h["design_endpoint"], "/_design_fn")
            self.assertIn("British Accent", self.client(fake).voice_options()["accent"])

    def test_design_request_maps_labels_and_never_forces_duration(self):
        with FakeOmniVoice() as fake:
            r = self.client(fake).synthesize(TEXT, DESIGN, self.out)
            endpoint, data = fake.calls[-1]
            self.assertEqual(endpoint, "_design_fn")
            self.assertEqual(data[0], TEXT)
            self.assertEqual(data[1], "English")
            self.assertIn("Male / 男", data)
            self.assertIn("British Accent / 英国口音", data)
            self.assertIsNone(data[6])                    # Duration (seconds) left unset
            self.assertAlmostEqual(r.duration, 2.0, places=2)
            self.assertEqual(r.sample_rate, 24000)
            self.assertEqual(r.status, "Done.")

    def test_clone_uploads_reference(self):
        with FakeOmniVoice() as fake:
            ref = Path(self.tmp.name) / "ref.wav"
            from tests.fake_omnivoice import wav_bytes
            ref.write_bytes(wav_bytes())
            voice = ov.VoiceSpec(mode="clone", reference_audio=str(ref), reference_text="Reference words.")
            self.client(fake).synthesize(TEXT, voice, self.out)
            self.assertEqual(fake.uploads, 1)
            endpoint, data = fake.calls[-1]
            self.assertEqual(endpoint, "_clone_fn")
            self.assertEqual(data[2]["path"], "/tmp/fake/upload/ref.wav")
            self.assertEqual(data[3], "Reference words.")

    def test_invalid_responses(self):
        cases = {"bad_json": ov.OmniVoiceProtocolError, "no_event_id": ov.OmniVoiceProtocolError,
                 "error_event": ov.OmniVoiceGenerationError, "bad_status": ov.OmniVoiceGenerationError,
                 "contract_changed": ov.OmniVoiceContractError}
        for mode, error in cases.items():
            with self.subTest(mode=mode), FakeOmniVoice() as fake:
                fake.mode = mode
                with self.assertRaises(error):
                    self.client(fake).synthesize(TEXT, DESIGN, self.out)

    def test_timeout(self):
        with FakeOmniVoice() as fake:
            fake.mode = "slow"
            with self.assertRaises(ov.OmniVoiceTimeout):
                self.client(fake, timeout=1).synthesize(TEXT, DESIGN, self.out)

    def test_silent_output_is_rejected(self):
        with FakeOmniVoice() as fake:
            fake.mode = "silent"
            with self.assertRaisesRegex(audio_probe.AudioValidationError, "silent"):
                self.client(fake).synthesize(TEXT, DESIGN, self.out)

    def test_invalid_voice_attribute(self):
        with FakeOmniVoice() as fake:
            bad = ov.VoiceSpec(mode="design", design={"accent": "Martian Accent"})
            self.assertTrue(self.client(fake).validate_voice(bad))
            with self.assertRaises(ov.OmniVoiceContractError):
                self.client(fake).synthesize(TEXT, bad, self.out)

    def test_implausible_speech_rate_is_rejected(self):
        with FakeOmniVoice() as fake:
            long_text = " ".join(["word"] * 40)          # 40 words in 2 s = 20 words/s
            with self.assertRaisesRegex(audio_probe.AudioValidationError, "words/s"):
                self.client(fake).synthesize(long_text, DESIGN, self.out)

    def test_duration_is_measured_not_estimated(self):
        with FakeOmniVoice() as fake:
            r = self.client(fake).synthesize(TEXT, DESIGN, self.out)
            self.assertEqual(r.duration, audio_probe.probe(self.out)["duration"])


if __name__ == "__main__":
    unittest.main()
