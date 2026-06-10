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

This project covers unofficial student knowledge about the Rutgers University Computer Science program. 

Official Rutgers resources provide course descriptions, degree requirements, and academic policies, but they do not capture the experiences, opinions, and advice that students share with one another. 
Students frequently discuss topics such as course difficulty, professor quality, elective recommendations, research opportunities, internship preparation, and strategies for succeeding in the major.
This information is often spread across Reddit posts, student blogs, and community resources rather than official university websites. 

The goal of this system is to aggregate that student-generated knowledge into a searchable question-answering system. 
By using retrieval-augmented generation (RAG), the system can answer questions using real student experiences while providing source attribution so users can trace answers back to the original documents. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Why these choices fit your documents:**

The document collection consists primarily of Reddit discussions, student advice posts, and long-form guidance articles.
These documents are generally written in paragraphs and discussion comments rather than formal sections with headings and subsections. 

I used a chunk size of 500 characters because it is large enough to preserve complete recommendations, opinions, and explanations while remaining small enough for precise retrieval.
A smaller chunk size would risk separating related ideas across multiple chunks, while a larger chunk size would combine unrelated topics and reduce retrieval accuracy. 

I used a 100-character overlap to reduce information loss at chunk boundaries.
Many recommendations and explanations span multiple sentences, and overlap helps ensure that important context is preserved even when content falls near the edge of a chunk. 

Before chunking, the ingestion pipeline performed preprocessing steps including HTML unescaping, whitespace normalization, removal of excessive line breaks, and cleaning of formatting artifacts from the source documents. 
Metadata such as source filename, title, URL, and chunk position were preserved for later attribution. 

**Final chunk count:** 145

### Sample Chunks (5 Random Chunks)

**[student_success_experiences.txt_chunk_9]**

Source : student_success_experiences.txt

Title  : Succeeding in Rutgers CS

Chunk# : 9

Length : 502

Text   : out of their own insecurities. Don’t let that become an insecurity of yours.
Just because someone is loud and outspoken does not mean they are right.
Tech has a long way to go when it comes to being inclusive. Educate yourself on this, and do not shy...

───────────────────────────

**[newcomer_guide.txt_chunk_12]**

Source : newcomer_guide.txt

Title  : For newcomers interested in C.S.

Chunk# : 12

Length : 502

Text   : look up a walkthrough on YouTube for creating a chat application; once you’ve completed a project, you can add your work to GitHub and your Resume.
For people who want to start their coding interview practice, I recommend looking at NeetCode to prep...

───────────────────────────

**[best_worst_professors.txt_chunk_2]**

Source : best_worst_professors.txt

Title  : Best CS Professors and worst CS Professors?

Chunk# : 2

Length : 294

Text   : and Francisco are sus

Santosh is smart and helpful enough, but def harder than the other profs imo.

Cowan is a king, Menny sucks

My favorite post here is Cowan roasting wrong answers on Chegg at the height of Covid cheating. 
He's simply the best
...

───────────────────────────

**[advice_from_senior.txt_chunk_2]**

Source : advice_from_senior.txt

Title  : My path through Rutgers CS, and advice for other undergrads, as a senior graduating in May

Chunk# : 2

Length : 501

Text   : Electives will have a '>' in front of them.

CS 112: A fairly implementation-based course. However, the data structures you learn here remain important throughout your CS career, so you should take the extra time to understand how exactly they work. ...

───────────────────────────

**[advice_from_senior.txt_chunk_23]**

Source : advice_from_senior.txt

Title  : My path through Rutgers CS, and advice for other undergrads, as a senior graduating in May

Chunk# : 23

Length : 503

Text   : can figure out how to tackle a novel problem. Figure out which kind your professor is early on, and adapt your studying habits accordingly.

Look out for Topics classes. Despite the high course numbers (442+ in my experience), these classes often hav...

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

I selected all-MiniLM-L6-v2 because it is lightweight, runs locally without requiring API calls, and is widely used for semantic retrieval tasks. 
The model provides a strong balance between retrieval quality and computational efficiency, making it well suited for this project.

**Production tradeoff reflection:**

If I were deploying this system for real users and cost was not a constraint, I would consider larger embedding models that provide stronger semantic understanding and retrieval accuracy. 
Important tradeoffs would include retrieval quality, inference latency, multilingual support, memory requirements, and hosting costs. 

A larger embedding model could potentially improve retrieval performance on nuanced questions about courses, professors, and student experiences. 
However, larger models would increase response times and infrastructure requirements. 
I would also consider whether users might ask questions in multiple languages and whether a model with stronger multilingual capabilities would be beneficial. 
Finally, I would evaluate whether a locally hosted solution or an API-hosted solution offered the best balance between performance, reliability, and maintenance. 

### Retrieval Tests (3 Queries with Top 5 Chunks)

══════════════════════════════════════════════════════════════════════
  **QUERY 1: 'What are some easier CS electives recommended by students?'**
══════════════════════════════════════════════════════════════════════

  **Result 1  |  similarity: 0.7013  |  distance: 0.2987**

  **Source  : easy_cs_electives.txt**

  Title   : What are the easiest electives for the BS Computer Science degree?

  Chunk # : 0

  URL     : https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/

  ID      : easy_cs_electives.txt_chunk_0

  Title is self-explanatory, but which electives that count towards the BS Computer Science degree are the easiest/require the least effort?  COMMENTS:  If Python and ML are what interest you, take CS 210 and CS 439.  Both those classes are relatively straightforward.  336 is straightforward as well.  Other than that, however, most CS electives are meant to be time consuming and project heavy (class...

───────────────────────────

  **Result 2  |  similarity: 0.6513  |  distance: 0.3487**

  **Source  : courses_by_difficulty.txt**

  Title   : CS classes by difficulty
  
  Chunk # : 0
  
  URL     : https://www.reddit.com/r/rutgers/comments/kcpdse/cs_classes_by_difficulty/
  
  ID      : courses_by_difficulty.txt_chunk_0

  Guys I have seen posts ranking CS electives by toughness. But I have never seen anyone rank the difficulty of the required classes.  CS : 01:198:111, 112, 205, 206, 211, 344.  Math : 01:640:151(Calc 1), 152(Calc 2), 250(Linear Algebra.  I would really appreciate if you could rate the classes by difficulty on a scale of 1-10 and if you could specify what classes to not take together in the same sem...

───────────────────────────

  **Result 3  |  similarity: 0.6441  |  distance: 0.3559**

  **Source  : advice_from_senior.txt**

  Title   : My path through Rutgers CS, and advice for other undergrads, as a senior graduating in May
  
  Chunk # : 1
  
  URL     : https://www.reddit.com/r/rutgers/comments/kgnpiv/my_path_through_rutgers_cs_and_advice_for_other/
  
  ID      : advice_from_senior.txt_chunk_1

  some grad classes, so you can take it a little slower and be fine.  APs: CS 111, Math 151+152  Freshman Fall: No CS classes  Freshman Spring: 112, 205  Sophomore Fall: 206, 211  Sophomore Spring: 213, 344, 352  Junior Fall: 314, 442  Junior Spring: 440, 443, 513  Senior Fall: 431, 444, 514  Senior Spring: none (a math elective but I haven't been listing those)  ------  Course-Teacher combination r...

───────────────────────────

  **Result 4  |  similarity: 0.6104  |  distance: 0.3896**

  **Source  : cs_success.txt**

  Title   : Guest

  Chunk # : 8

  URL     : https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb

  ID      : cs_success.txt_chunk_8

  You can ask any upperclassman what they think the most important CS course is, and Data Structures will almost certainly be one of their top 3.  The Story of 50% of the students in CS112 Now, let me tell you the story of Alice. Alice is a metaphorical student that represents 50% of the CS112 roster.  Alice took CS111, did fairly well in it (got better than a B). In 111, Alice often found it hard t...

───────────────────────────

  **Result 5  |  similarity: 0.5982  |  distance: 0.4018**

  **Source  : easy_cs_electives.txt**
  
  Title   : What are the easiest electives for the BS Computer Science degree?
  
  Chunk # : 1
  
  URL     : https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/
  
  ID      : easy_cs_electives.txt_chunk_1

  461, 440, 213, 214).  However, even though those classes can be hard, they can prove useful for your career.  CS 336: Prin Info/ Data Mgmt Philosophy Minds, Machines Persons: Can only do 2 non-CS electives total to count towards BS. This is a pretty light, fun, and easy one. Math 354 Linear Optimization: Requires little knowledge of linear algebra if you forgot it. Pretty decently easy course, req...

───────────────────────────

**Why These Chunks Are Relevant:**
The retrieved chunks include direct discussions of CS electives and course difficulty from student forums. 
The first result specifically lists CS 210, CS 429, and CS 336 as relatively straightforward electives, which directly matches the query about easier CS courses.
Additional chunks from "courses_by_difficulty" and "advice_from_senior" provide supporting context about course structure and difficulty comparisons, even though they are less directly focused on electives. 
Together, they collectively cover both explicit recommendations and broader difficulty-based classification, which helps the model synthesize a more complete answer. 

══════════════════════════════════════════════════════════════════════
  **QUERY 2: 'What courses do students frequently describe as among the most difficult Rutgers CS courses?'**
══════════════════════════════════════════════════════════════════════

  **Result 1  |  similarity: 0.6764  |  distance: 0.3236**

  **Source  : newcomer_guide.txt**

  Title   : For newcomers interested in C.S.

  Chunk # : 8

  URL     : https://www.reddit.com/r/rutgers/comments/190uh5j/for_newcomers_interested_in_cs/

  ID      : newcomer_guide.txt_chunk_8

  (Example Syllabus).  Ultimately, I have not put too much into this section because the electives are mostly personal preferences. Some courses are more complex than others but generally similar by course level. However, I strongly recommend utilizing RateMyProfessor as some professors teach better than others and can make the same course significantly more straightforward to complete.  Career Deve...

───────────────────────────

  **Result 2  |  similarity: 0.6508  |  distance: 0.3492**

  **Source  : easy_cs_electives.txt**

  Title   : What are the easiest electives for the BS Computer Science degree?

  Chunk # : 6

  URL     : https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/

  ID      : easy_cs_electives.txt_chunk_6

  to check off math requirements as well, since it is extremely tedious, although not conceptually hard.  I mean most math courses are tedious, especially since the upper level math takes like 30 minutes for 1 problem. But yeah definitely something to avoid if you're not strong in math or looking for a math degree. Still definitely an easier course than a lot of other CS electives  Is Rutgers CS mor...

───────────────────────────

  **Result 3  |  similarity: 0.6458  |  distance: 0.3542**

  **Source  : courses_by_difficulty.txt**

  Title   : CS classes by difficulty

  Chunk # : 0

  URL     : https://www.reddit.com/r/rutgers/comments/kcpdse/cs_classes_by_difficulty/

  ID      : courses_by_difficulty.txt_chunk_0

  Guys I have seen posts ranking CS electives by toughness. But I have never seen anyone rank the difficulty of the required classes.  CS : 01:198:111, 112, 205, 206, 211, 344.  Math : 01:640:151(Calc 1), 152(Calc 2), 250(Linear Algebra.  I would really appreciate if you could rate the classes by difficulty on a scale of 1-10 and if you could specify what classes to not take together in the same sem...

───────────────────────────

  **Result 4  |  similarity: 0.6197  |  distance: 0.3803**

  **Source  : newcomer_guide.txt**

  Title   : For newcomers interested in C.S.

  Chunk # : 7

  URL     : https://www.reddit.com/r/rutgers/comments/190uh5j/for_newcomers_interested_in_cs/

  ID      : newcomer_guide.txt_chunk_7

  and C.S. major (once you have declared it).  Sample B.A. Schedule (rutgers.edu)  Sample B.S. Schedule (rutgers.edu)  Picking Classes  There are a lot of C.S. electives to choose from. You can pick and choose which electives you want to do. Do your research by looking at this subreddit and Google. Some courses also have their Syllabus listed publicly (before the class starts) if you search it on Go...

───────────────────────────

  **Result 5  |  similarity: 0.6125  |  distance: 0.3875**

  **Source  : cs_success.txt**

  Title   : Guest

  Chunk # : 8

  URL     : https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb

  ID      : cs_success.txt_chunk_8

  You can ask any upperclassman what they think the most important CS course is, and Data Structures will almost certainly be one of their top 3.  The Story of 50% of the students in CS112 Now, let me tell you the story of Alice. Alice is a metaphorical student that represents 50% of the CS112 roster.  Alice took CS111, did fairly well in it (got better than a B). In 111, Alice often found it hard t...

══════════════════════════════════════════════════════════════════════
  **QUERY 3: 'How do students recommend finding research opportunities within Rutgers Computer Science?'**
══════════════════════════════════════════════════════════════════════

  **Result 1  |  similarity: 0.7172  |  distance: 0.2828**

  **Source  : cs_research_opportunities.txt**

  Title   : CS Research Opportunities

  Chunk # : 1

  URL     : https://www.reddit.com/r/rutgers/comments/152i9se/cs_research_opportunities/

  ID      : cs_research_opportunities.txt_chunk_1

  I met all the prerequisites for).  Also, I couldn't apply for the summer research program this year due to my summer classes.  So, I'm wondering if any of you have any suggestions for finding research opportunities. Thanks!  COMMENTS:  Sometimes the Rutgers CS department emails out notifications about new jobs. These include student programmers and CS research assistant positions.  If you do not g...

───────────────────────────

  **Result 2  |  similarity: 0.6070  |  distance: 0.3930**

  **Source  : cs_success.txt**

  Title   : Guest

  Chunk # : 30

  URL     : https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb

  ID      : cs_success.txt_chunk_30

  you find jobs and offer you their couches.  Rutgers is a great place to study Computer Science, and I hope your time there will be as memorable as mine was.

───────────────────────────

  **Result 3  |  similarity: 0.6059  |  distance: 0.3941**

  **Source  : cs_success.txt**

  Title   : Guest

  Chunk # : 29

  URL     : https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb

  ID      : cs_success.txt_chunk_29

  Join the USACS board, and help plan events. Hang out at the CAVE and help underclassmen understand difficult concepts. Help the noobs out at hackathons.  Make friends out of your peers. Impossible looking homework assignments will become easier. You’ll spend a silly amount of timeworking on a CTF challenge, or writing a game. You’ll get one letter Github usernames together. After college, they’ll ...

───────────────────────────

  **Result 4  |  similarity: 0.5740  |  distance: 0.4260**

  **Source  : newcomer_guide.txt**

  Title   : For newcomers interested in C.S.

  Chunk # : 9

  URL     : https://www.reddit.com/r/rutgers/comments/190uh5j/for_newcomers_interested_in_cs/

  ID      : newcomer_guide.txt_chunk_9

  When I came to Rutgers, my goal was and still is to set myself up for success in the future. Everyone will talk about internships or research and the importance of it.  The real question is, how do I obtain those opportunities? The answer I’ve found so far is developing yourself to “sell” yourself to companies. Taking the initiative is always looked highly upon.  At Rutgers, there are a lot of opp...

───────────────────────────

  **Result 5  |  similarity: 0.5517  |  distance: 0.4483**
  
  **Source  : cs_research_opportunities.txt**
  
  Title   : CS Research Opportunities
  
  Chunk # : 4
  
  URL     : https://www.reddit.com/r/rutgers/comments/152i9se/cs_research_opportunities/
  
  ID      : cs_research_opportunities.txt_chunk_4

  Cold email professors who have research projects. It doesn't have to be CS professors cuz most labs will benefit from some coding and stuff so if you happen to be interested in biology or chemistry go do some research there also because there is a lot of data analytics and stuff they use. Also, you gotta be alright with doing free labor in research. You'll have better odds doing research with a pr...

───────────────────────────

**Why These Chunks Are Relevant:**
The top retrieved chunks come from posts discussing research opportunities, student experiences, and departmental advice. 
The highest-ranked chunk explicitly mentions job postings, research assistant positions, and methods like email notifications and applications, which directly match the question.
Additional chunks reinforce this with strategies such as cold emailing professors, joining organizations like USACS, and building connections. Even though some chunks focus on general career advice, they still contribute relevant context about how students obtain research positions at Rutgers CS. 

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system uses a strict grounding prompt that explicitly forbids the language model from using outside knowledge. 
The prompt includes instructions such as: 
1. Answer only using information found in the provided context documents. 
2. Do not use outside knowledge, training data, or assumptions.
3. If the document do not contain enough information to answer the question, respond with: "I don't have enough information in the provided documents."
4. Cite sources using the format [Source: filename].
5. Never fabricate sources.

The retrieved chunks are inserted into the prompt as a structured context block before the user's question is sent to the model. 

**How source attribution is surfaced in the response:**

Each retrieved chunk is formatted with metadata headers containing the source filename, title, and URL. 
The language model is instructed to cite source filenames directly in its response using inline citations such as [Source: easy_cs_electives.txt]. 

In addition, the application programmatically displays a separate list of retrieved source documents beneath every answer (along with the urls). 
This ensure that source attribution is always visible even if the model's response itself is brief. 

The system retrieves the top 5 relevant chunks from ChromaDB before generation. 
Because only retrieved content is provided to the model and the prompt explicitly forbids outside knowledge, answers remain grounded in the document collection rather than the model's general training data. 

### System Responses (2 Example Outputs + 1 Refusal Output)

**Q: What are the easiest CS electives at Rutgers?**

A: According to the provided context documents, the easiest CS electives at Rutgers are: 
CS 210, CS 439, and CS 336, as they are described as "relatively straightforward" [Source: easy_cs_electives.txt]. 

Additionally, it is recommended to use RateMyProfessor to find professors who teach well and can make a course easier to complete [Source: newcomer_guide.txt]. 

Note that the difficulty of a course can also depend on personal preferences and the student's strengths [Source: newcomer_guide.txt].

Retrieved From: 

• newcomer_guide.txt (https://www.reddit.com/r/rutgers/comments/190uh5j/for_newcomers_interested_in_cs/)

• easy_cs_electives.txt (https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/)

• courses_by_difficulty.txt (https://www.reddit.com/r/rutgers/comments/kcpdse/cs_classes_by_difficulty/)

**Q: How do students succeed in Rutgers CS?**

A: To succeed in Rutgers CS, students should develop a good mental model of programming early on, as their performance in intro courses is incredibly important [Source: cs_success.txt]. Additionally, joining the USACS board, participating in events, and helping underclassmen can be beneficial [Source: cs_success.txt]. Making friends with peers can also make homework assignments easier and provide opportunities for collaboration and support [Source: cs_success.txt]. Furthermore, seeking help from Sesh, TAs, peers, and people at the iLabs when needed can also contribute to success [Source: cs_success.txt].

Retrieved From: 

• student_success_experiences.txt (https://github.com/sakib/succeeding_in_rutgers_cs)

• cs_success.txt (https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb)

• cs_quality.txt (https://www.reddit.com/r/rutgers/comments/1bod56d/the_quality_of_computer_science_at_rutgers/)

**Q: What is the salary of a Rutgers CS graduate in 2026?**

A: I don't have enough information in the provided documents.

Retrieved From: 

• cs_quality.txt (https://www.reddit.com/r/rutgers/comments/1bod56d/the_quality_of_computer_science_at_rutgers/)

• student_success_experiences.txt (https://github.com/sakib/succeeding_in_rutgers_cs)

• cs_success.txt (https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb)

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What courses do students frequently describe as among the most difficult Rutgers CS courses? | Students commonly identify CS112 and CS344 as particularly difficult courses. | The system correctly identified CS112 as one of the most difficult courses based on student discussion, and referenced Data Structures as a key challenging course. However, it did not explicitly isolate a full ranked list of difficult courses like CS344. | Relevant | Partially Accurate |
| 2 | What advice do students repeatedly give for succeeding in Rutgers Computer Science? | Students commonly recommend starting projects early, attending lectures consistently, and practicing programming outside of class. | The system emphasized early development of programming fundamentals, joining CS organizations (like USACS), collaborating with peers, and seeking help. It also highlight networking and proactive engagement as success strategies. | Relevant | Accurate |
| 3 | Which minors are commonly recommended alongside a Computer Science major? | Mathematics and statistics are frequently recommended complementary minors. | The system correctly identified Mathematics and Statistics as recommended minors, and also included related fields such as Data Science and other interdisciplinary minors. | Relevant | Accurate |
| 4 | What are some easier CS electives recommended by students? | Students frequently mention CS210, CS336, and CS439 as relatively easier electives. | The system correctly listed CS210, CS336, and CS439 as easier electives. It also added other perceived "easy" courses such as CS314 and some non-CS electives. | Relevant | Accurate |
| 5 | How do students recommend finding research opportunities within Rutgers Computer Science? | Students recommend contacting professors directly, building relationships during courses, and reaching out about ongoing research projects. | The system provided a detailed set of strategies including checking CS department postings, cold emailing professors, joining labs, gaining experience first, and building professional relationships. | Relevant | Accurate |

**Retrieval quality:** Relevant  
**Response accuracy:** Accurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What are the best professors?

**What the system returned:**

The system returned a long list of professor names from multiple sources, including some duplicate names and inconsistent spellings. 
Rather than synthesizing the most commonly recommended professors, it largely reproduced names that appeared in the retrieved documents. 

**Root cause (tied to a specific pipeline stage):**

This issue originated primarily in the retrieval and generation stages.
The query "best professors" is broad and subjective, causing retrieval to return chunks containing many different opinions.
Because the source documents were discussion threads with multiple commenters, the retrieved chunks contained long lists of professor names without a clear ranking or consensus. 

The generation model was grounded correctly, but it lacked a mechanism for determining which professors were mentioned most frequently or most positively. 
As a result, it summarized nearly every retrieved name instead of identifying a smaller set of commonly recommended professors. 

**What you would change to fix it:**

I would improve the retrieval pipelin by adding metadata filtering or reranking to prioritize chunks with stronger consensus. 
I would also aggregate professor mentions across multiple retrieved chunks before generation so that the model can identify trends rather than simply repeating names. 
Another improvement would be increasing chunk size slightly so that positive and negative opinions remain grouped together, providing more complete context for the model. 

---

## Query Interface

**Interface Overview**
The system provides a simple web-based interface built with Gradio. 
Users enter a natural language question in a single text input box and receive two outputs:

1. Answer Output: A grounded response generated by a retrieval-augmented language model
2. Retrieved Sources: A list of the unique source documents used to generate the answer, displayed with filenames and URLs

The interface is designed to ensure transparency by showing exactly which documents contributed to the response. 

The backend pipeline performs the following steps: 

1. Accepts user question
2. Retrieves top-k relevant chunks from a vector database (ChromaDB)
3. Formats retrieved chunks with metadata (source, title, URL)
4. Sends grounded context & question to the LLM
5. Returns generated answer & unique source list

**Input/Output Fields**

Input: 
- Your Question: Natural language question about Rutgers CS topics (courses, electives, research, etc.)

Outputs: 
- Answer: LLM-generated response strictly grounded in retrieved documents
- Retrieved From: Bullet list of unique source filenames & URLs used in retrieval

**Sample Interaction Transcript**

User Input: What are some easier CS electives recommended by students?

System Output: 

Answer: 

According to students, some easier CS electives are CS 210, CS 439, and CS 336 [Source: easy_cs_electives.txt]. Additionally, CS 314: Principles of Programming languages is also considered easy when taught [Source: easy_cs_electives.txt]. Non-CS electives that are considered easy and can count towards the BS degree include Philosophy: Minds, Machines, Persons and Math 354: Linear Optimization [Source: easy_cs_electives.txt].

Retrieved From: 

• easy_cs_electives.txt (https://www.reddit.com/r/rutgers/comments/1991tq0/what_are_the_easiest_electives_for_the_bs/)
• courses_by_difficulty.txt (https://www.reddit.com/r/rutgers/comments/kcpdse/cs_classes_by_difficulty/)
• advice_from_senior.txt (https://www.reddit.com/r/rutgers/comments/kgnpiv/my_path_through_rutgers_cs_and_advice_for_other/)
• cs_success.txt (https://medium.com/@rutgersusacs/guest-post-succeeding-in-rutgers-computer-science-by-v-48e6a5b75efb)


---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning document provided a clear roadmap for the entire project before any code was written. 
Defining the chunking strategy, retrieval approach, evaluation questions, and anticipated challenges early made it easier to make implementation decisions later. 
The evaluation plan was particularly useful because is established concrete questions that could be used to verify retrieval quality and grounding behavior. 

**One way your implementation diverged from the spec, and why:**

One area where the implementation diverged slightly from the original plan was the generation stage. While the planning document focused primarily on source attribution and grounding, the final implementation used a much stricter system prompt than originally described. 
During testing, I found that weaker prompts sometimes encouraged the model to supplement answers with general knowledge.
Strengthening the prompt improved grounding behavior and helped ensure that unsupported questions produced refusal responses rather than hallucinated answers. 

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

- *What I gave the AI:* I provided my planning.md document, including the Chunking Strategy section, Retrieval Approach section, and architecture diagram. I asked the AI to generate the ingestion pipeline that would load text documents, clean them, split them into 500-character chunks with 100-character overlap, preserve metadata, and save the results to chunks.json. 
- *What it produced:* The AI generated a Python ingestion pipeline containing document loading functions, text cleaning logic, chunking functions, metadata handling, and JSON export functionality. 
- *What I changed or overrode:* I reviewed the generated code and modified several implementation details, including metadata preservation and output formatting. I also added additional comment and verification steps to ensure that chunk boundaries, overlap size, and metadata fields matched the specifications defined in planning.md. 

**Instance 2**

- *What I gave the AI:* I provided the Milestone 5 requirements, my architecture diagram, and the grounding requirements for retrieval-augmented generation. I asked the AI to generate code that connected retrieval to a Groq-hosted Llama model and created a Gradio interface with source attribution.
- *What it produced:* The AI generated an application that retrieved relevant chunks from ChromaDB, constructed a context block, called the Groq API, and displayed answers and sources in a Gradio web interface. 
- *What I changed or overrode:* I carefully reviewed the grounding prompt and strengthened it so that the model was explicitly forbidden from using outside knowledge. I also verified that source attribution was programmatically surfaced through the interface and tested out-of-scope questions to ensure the model returned refusal responses when the retrieved documents did not contain enough information. 
