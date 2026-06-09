# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project focuses on student-generated knowledge about the Rutgers University Computer Science program. 
The document collection includes discussions about professors, course difficulty, electives, research opportunities, academic planning, internships, and strategies for success in the major. 

This information is valuable because official Rutgers course desciptions and department resources provide limited insight into the actual student experience.
Students frequently share advice, opinion, and experiences through Reddit discussions, blog posts, and community resources, but this knowledge is scattered across many different sources and can be difficult for students to find efficiently.
The goal of this project is to make that unofficial Rutgers CS knowledge searchable through a retrieval-augmented generation (RAG) system.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Best and Worst CS Professors | https://www.reddit.com/r/rutgers/comments/u2bock/best_cs_professors_and_worst_cs_professors/ |
| 2 | Reddit | Quality of CS at Rutgers | https://www.reddit.com/r/rutgers/comments/1bod56d/the_quality_of_computer_science_at_rutgers/ |
| 3 | Reddit | Rutgers CS Courses by Difficulty | https://www.reddit.com/r/rutgers/comments/kcpdse/cs_classes_by_difficulty/ |
| 4 | Reddit | Easiest Rutgers CS Electives | https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/ |
| 5 | Reddit | Advice from a Graduating Senior | https://www.reddit.com/r/rutgers/comments/kgnpiv/my_path_through_rutgers_cs_and_advice_for_other/ |
| 6 | Reddit | CS Research Opportunities | https://www.reddit.com/r/rutgers/comments/152i9se/cs_research_opportunities/ |
| 7 | Reddit | Minor Recommendations | https://www.reddit.com/r/rutgers/comments/1fioy6g/people_with_computer_science_majors_what_minors/ |
| 8 | Reddit | Newcomer's Guide | https://www.reddit.com/r/rutgers/comments/190uh5j/for_newcomers_interested_in_cs/ |
| 9 | Medium | Success in Rutgers CS | https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb |
| 10 | Github | Student Experiences of Succeeding in Rutgers CS | https://github.com/sakib/succeeding_in_rutgers_cs |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
