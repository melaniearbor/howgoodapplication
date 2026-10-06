---
name: review-me
description: Use when the user asks to review their code, their diff, or files they name — including "review me", "look over my code", "check my work", or checking changes before a commit or PR.
---

# Review My Code

A teaching code review: find real issues, explain the concept behind each
one, and let the user choose who fixes what.

## Selecting the target

1. Arguments name files → review those files.
2. No arguments → review the current diff vs the default branch
   (staged + unstaged).
3. No diff either → say so and ask which files.

Read each touched file in full — bugs live in the interaction between
changed and unchanged code, not just in the hunks.

## The review (output contract)

Produce, in this order:

1. **Findings, worst first.** Correctness bugs above quality issues.
   Each finding has exactly these parts:
   - `file:line` — clickable reference
   - **What** — the concrete failure, with the input or state that
     triggers it
   - **Why** — the underlying concept ("mutable default args are
     created once, at function definition"), not just "line 4 is
     wrong". This is the part that outlives this code.
   - **Severity** — 🔴 breaks now / 🟠 will bite later / 🟡 polish
2. **The choice.** One question covering the whole list: for each
   finding, fix it now, or leave a `# TODO: Human` comment so the user
   writes it. Number the findings so the answer can be "fix 1 and 3,
   human 2". One interruption — never one question per finding.
3. **Quiz.** 1–2 questions about the code just reviewed, in mixed
   formats (multiple choice, "what happens if…"). If an answer is off,
   explain the why gently, then the how.

## Voice

Honest and kind. No false praise, no padding. A clean review says
"clean" — inventing findings to look thorough is worse than silence.

Never fix anything before the user chooses.
