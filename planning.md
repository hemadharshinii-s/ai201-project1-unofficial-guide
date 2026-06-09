# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This project builds an unofficial guide to the Rutgers University Computer Science program. 
While official Rutgers resources provide degree requirements, course descriptions, and academic policies, they often do not capture the experiences, opinions, and advice shared by students.
This project collects student-generated knowledge from Reddit discussions, student guides, and community resources to help answer questions about professors, course difficulty, electives, research opportunities, academic success, and navigating the Rutgers CS program. 

This knowledge is valuable because much of it is scattered across forum posts, student blogs, and discussion threads, making it difficult for students to locate and compare information efficiently. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Best and Worst CS Professors: Student opinions about the best and worst Rutgers CS professors | https://www.reddit.com/r/rutgers/comments/u2bock/best_cs_professors_and_worst_cs_professors/ |
| 2 | Reddit | Quality of CS at Rutgers: Student perspectives on the overall quality and reputation of Rutgers Computer Science | https://www.reddit.com/r/rutgers/comments/1bod56d/the_quality_of_computer_science_at_rutgers/ |
| 3 | Reddit | Rutgers CS Courses by Difficulty: Student discussions ranking Rutgers CS and mathematics courses by difficulty | https://www.reddit.com/r/rutgers/comments/kcpdse/cs_classes_by_difficulty/ |
| 4 | Reddit | Easiest Rutgers CS Electives: Student recommendations regarding easier Rutgers CS electics | https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/ |
| 5 | Reddit | Advice from a Graduating Senior: Senior student's academic path through Rutgers CS, course sequencing, and recommendations for undergraduates | https://www.reddit.com/r/rutgers/comments/kgnpiv/my_path_through_rutgers_cs_and_advice_for_other/ |
| 6 | Reddit | CS Research Opportunities: Advice and experiences related to finding research opportunities within Rutgers Computer Science | https://www.reddit.com/r/rutgers/comments/152i9se/cs_research_opportunities/ |
| 7 | Reddit | Minor Recommendations: Recommendations for minors that complement a Computer Science major | https://www.reddit.com/r/rutgers/comments/1fioy6g/people_with_computer_science_majors_what_minors/ |
| 8 | Reddit | Newcomer's Guide: Comprehensive introductory guide for students interested in Rutgers Computer Science | https://www.reddit.com/r/rutgers/comments/190uh5j/for_newcomers_interested_in_cs/ |
| 9 | Medium | Success in Rutgers CS: Common patterns for success and failure in Rutgers Computer Science | https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb |
| 10 | Github | Student Experiences of Succeeding in Rutgers CS: Long-form relections and advice from a Rutgers CS graduate (and others) about succeeding in the program | https://github.com/sakib/succeeding_in_rutgers_cs |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:** 

The document collection consists primarily of Reddit discussions, student advice posts, and long-form guidance articles. 
These sources contain information organized into short paragraphs and discussion comments rather than formal sections.

I will use a chunk size of 500 characters with an overlap of 100 characters.
This size is large enough to preserve complete thoughts and recommendations while remaining focused enough for semantic retrieval. 
The overlap helps prevent important information from being split between chunk boundaries, especially when a recommendation or explanation spans multiple sentences.

Chunks that are too small may lose context and retrieve incomplete ideas. Chunks that are too large may contain multiple unrelated topics, making retrieval less precise.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5

**Production tradeoff reflection:**

This project will use the sentence-transformers embedding model all-MiniLM-L6-v2.
This model is lightweight, free to run locally, and commonly used for semantic search applications.

For each user query, the system will retrieve the top 5 most relevant chunks from ChromaDB before passing them to the language model. 

If this system were deployed in production, I would consider additional factors when selecting an embedding model. 
Larger models may provide higher retrieval accuracy but increase computational cost and latency.
Other considerations include multilingual support, memory requirements, inference speed, and performance on domain-specific educational content. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What courses do students frequently describe as among the most difficult Rutgers CS courses? | Students commonly identify CS112 and CS344 as particularly difficult courses. |
| 2 | What advice do students repeatedly give for succeeding in Rutgers Computer Science? | Students commonly recommend starting projects early, attending lectures consistently, and practicing programming outside of class. |
| 3 | Which minors are commonly recommended alongside a Computer Science major? | Mathematics and statistics are frequently recommended complementary minors. |
| 4 | What are some easier CS electives recommended by students? | Students frequently mention CS210, CS336, and CS439 as relatively easier electives. |
| 5 | How do students recommend finding research opportunities within Rutgers Computer Science? | Students recommend contacting professors directly, building relationships during courses, and reaching out about ongoing research projects. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Contradictory Student Opinions: Different students may provide conflicting recommendations about courses, professors, or academic strategies. Retrieval may surface multiple viewpoints that are difficult to summarize consistently. 

2. Retrieval Across Multiple Topics: The document collection covers many topics, including professors, electives, research, and academic success. Some queries may retrieve chunks from unrelated topics if the wording overlaps semantically.

3. Chunk Boundary Issues: Important information may be split across chunk boundaries, causing retrieval to return only part of the relevant context. 

4. Grounding Failures: The language model may attempt to answer from general knowledge rather than the retrieved context if grounding instructions are not sufficiently strict. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
                                                  Rutgers CS Sources
                                             (Reddit + Student Guides)
                                                            |
                                                            v
                                                  Document Ingestion
                                                  (Python File Loader)
                                                            |
                                                            v
                                                       Chunking
                                        (500 Character Chunks, 100 Overlap)
                                                            |
                                                            v
                                                       Embeddings
                                   (sentence-transformers: all-MiniLM-L6-v2)
                                                            |
                                                            v
                                                       ChromaDB
                                                  (Vector Database)
                                                            |
                                                            v
                                                       Retrieval
                                                  (Top-k Semantic Search)
                                                            |
                                                            v
                                                       Generation
                                             (Groq Llama-3.3-70B-Versatile)
                                                            |
                                                            v
                                                  Answer + Source Citations
```

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

I plan to use ChatGPT, Claude, and Gemini as implementation assistants throughout the project.
The AI tools will help generate code based on the specifications I define in this planning document, but I will review, test, and modify all generated code before using it. 

**Milestone 3 — Ingestion and chunking:**

- Document Ingestion and Chunking: I will provide the AI tools with my document collection description, chunk size, overlap size, and pipeline architecture. I will ask the AI to generate Python code that loads text files from the documents directory, performs basic cleaning, and creates chunks according to my specified strategy. 
   - Expected Output: File loading functions, text cleaning functions, chunking functions, metadata creation for source tracking

**Milestone 4 — Embedding and retrieval:**

- Embedding and Vector Store: I will provide the AI tools with the retrieval approach section of this plan and ask them to generate code that uses the all-MiniLM-L6-v2 embedding model and stores embeddings in ChromeDB. 
   - Expected Output: Embedding generation code, ChromaDB initialization, code for storing chunks and metadata, retrieval functions

**Milestone 5 — Generation and interface:**

- Grounded Generation: I will provide the AI tools with the project requirements related to grounding and source attribution. I will ask them to generate code that retrieves relevant chunks and constructs prompts that instruct the language model to answer only from retrieved context. 
   - Expected Output: Prompt templates, retrieval-to-generation, source attribution formatting, refusal handling for out-of-scope questions
- User Interface: I will provide the AI tools with the project requirements for a query interface and ask them to generate a simple Gradio application. 
   - Expected Output: Gradio interface code, input and output fields, and query handling functions

For every generated component, I will review the implementation, compare it against the project requirements, test the code, and modify it when necessary to ensure it matches my design decisions. 

