# Final-approval checklist: {{TOPIC}}

Owner decisions the Studio cannot take. The agent records each one only after the owner states it
(review/OWNER_APPROVALS.json, schema owner_approvals/1), with scope, source revision, date, evidence,
conditions and what invalidates it.

- [ ] **Claims**: approve the claims the film uses (review/EDITORIAL_APPROVAL_PACKAGE.md) for narration revision `…`.
- [ ] **Voice**: approve the narrator for THIS project and its publication purpose (config/tts_providers.json `voice_approvals`), unless it is already in `voices_cleared`.
- [ ] **Pronunciation**: accept the reviewed audio for the listed terms (review/PRONUNCIATION_REVIEW.md); the acceptance is bound to the audio revision.
- [ ] **Images and attribution**: confirm the archival images and the credits (review/RIGHTS_PROVENANCE.md).
- [ ] **Disclosure**: AI-generated narration stated in the description (review/YOUTUBE_DESCRIPTION.md).
- [ ] **Unused claims**: research-only claims stay in the archive; nothing used by the film may remain unapproved.
- [ ] **Publication**: request the publication evaluation (profile PUBLICATION_CANDIDATE) and the final render.

The Studio never uploads, merges or pushes. Publishing is the owner's action.
