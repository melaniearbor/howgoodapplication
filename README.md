# Why, hello!

`POST`ing to an endpoint is just about the most fun way to apply to a job ever. I'm just so tickled 🤭✨

There are several files in this repo:
- `send_resume.py` which is the code I ran to submit my resume to the aforementioned endpoint
- `test_send_resume.py` running against the dummy values in `.env.tests`, so the suite passes for any cloner
- `.gitignore` to enable the use of an `.env` file for secrets, and ignore additional other bits
- `requirements.txt` to install the needful
- `.claude/skills/review-me/SKILL.md` so cloners running Claude Code get `/review-me` skill I created too

The real `SECRET`, `ENDPOINT`, and `RESUME_URL` live in a local `.env`, which `.gitignore` keeps out of the repo. Cloners get the dummy stand-ins in `.env.tests` instead.

## Bot involvement (glm-5.3 from z.ai using Claude as the harness)

Mostly a tutor and reviewer — I asked it to teach, not do, and wrote nearly all the code myself.

- Explained HMAC signing when I'd never used it before
- Coached the design of the test suite without writing it for me
- Taught me `pytest.param`; I use `parametrize` frequently, but had never used `pytest.param`. You learn something new every day!
- Pair-debugged a git push error, a pytest parametrization `TypeError`, and the exception handling in `send_resume`
- Spell check
- Code review and feedback, partly via a `/review-me` skill I had it build (now in this repo)
- Sounding board for what to hide in `.env` versus commit as dummies in `.env.tests`