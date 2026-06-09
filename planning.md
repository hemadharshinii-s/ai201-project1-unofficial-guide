# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This project focuses on student-generated knowledge about the Rutgers University Computer Science program. 
The document collection includes discussions about professors, course difficulty, electives, research opportunities, academic planning, internships, and strategies for success in the major. 

This information is valuable because official Rutgers course desciptions and department resources provide limited insight into the actual student experience.
Students frequently share advice, opinion, and experiences through Reddit discussions, blog posts, and community resources, but this knowledge is scattered across many different sources and can be difficult for students to find efficiently.
The goal of this project is to make that unofficial Rutgers CS knowledge searchable through a retrieval-augmented generation (RAG) system.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
