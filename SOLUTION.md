# Solution Notes

## Environment
- Python version: 3.14.6
- Key libraries used: pandas (STANDARD analysis), requests (Ollama client), plus Python built-ins: csv, json, sqlite3, pathlib, collections.Counter
- LLM API used: Ollama (local, free, no API key)
- LLM model used: llama3.2

## Highest Level Completed

| Exercise | BASE | STANDARD | ADVANCED |
|----------|------|----------|----------|
| 1 - Python & Data | [x] | [x] | [ ] |
| 2 - SQL | [x] | [x] | [ ] |
| 3 - LLM | [x] | [x] | [ ] |
| 4 - Integration | [x] | [ ] | [ ] |

---

## Exercise 1: Data Handling

**Your approach:** Python was the first language I learned years ago, but I'd been mostly working with C++ since, so I had to re-learn the data side of it from scratch. For BASE I used pure Python with `csv.DictReader` (which I rediscovered while researching CSV helpers) to load the tickets into a list of dicts, then counted statuses with a dictionary, filtered by priority case-insensitively, and found tickets with empty descriptions. For STANDARD I switched to pandas, read the CSV, removed rows with empty descriptions, normalized priority to lowercase, parsed `created_at` into datetimes, then computed tickets per month, average resolution time per priority, and the category with the highest percentage of unresolved tickets.

**If you completed BASE:** The messy priority values (HIGH/high/High) were handled by comparing with `.lower()` on both sides, so the comparison ignores case.

**If you completed STANDARD:** My STANDARD code already works on whole columns at once (like `pd.to_datetime()` converting every date in a column in one go, or `groupby().mean()` computing all averages together), rather than touching rows one at a time. That's why it would still work fine on a much bigger dataset without changes. For a really large file, I would also tell `pd.read_csv` the type of each column in advance, and read the file in chunks so it isn't all loaded into memory at once.
---

## Exercise 2: SQL

**Your approach:** SQL wasn't new to me, but I hadn't used it in a while, so I had to revisit COUNT and JOINs. I wrote all queries for BASE and STANDARD. BASE covered a plain SELECT with sorting, a JOIN between employees and departments, and a grouped count. STANDARD added aggregation (AVG, SUM) with GROUP BY, HAVING to filter grouped results, and a LEFT JOIN to include departments with zero active projects.

**If you completed BASE:** The JOIN was the hardest query to re-learn because it required remembering how the `department_id` foreign key links employees to departments, and the `ON` condition syntax. Once I remembered that the join pairs rows where `employees.department_id = departments.id`, the rest followed.

**If you completed STANDARD:** For Query 6, I used a LEFT JOIN with the `active` condition inside the `ON` clause, so departments with no active projects still appear with a count of 0. An INNER JOIN would drop those departments entirely from the output, so those departments would vanish instead of showing 0.

---

## Exercise 3: LLM & Prompt Engineering

**Your approach:** This was completely new to me — I'd never called an LLM API before. I used Ollama running llama3.2 locally. BASE covered summary, sentiment classification, and question answering, each using a prompt with a clear instruction and an explicit output constraint. STANDARD used two prompt strategies to extract structured company data as JSON, then parsed the model output (stripping markdown code fences) into Python dicts.

**If you completed BASE:** The wording of the prompt changed the output format noticeably. For example, asking "is this positive or negative?" lets the model answer with a full sentence, but adding "Return only a single word" forces it to output just `positive`/`neutral`/`negative`. The model follows explicit instructions much more reliably than implicit ones.

**If you completed STANDARD:** Prompt v2 (the schema-driven prompt) worked better. Prompt v1 just listed the field names and asked for a JSON array; prompt v2 gave the model the exact JSON schema to copy, instructed it to use `null` for missing values, and forbade any extra text. Showing the model the exact output shape it should imitate produced more consistent, reliably parseable JSON than describing the shape in words.

---

## Exercise 4: Integration

**Your approach:** BASE read all documents from the folder, counted words, extracted keywords by frequency (excluding stop words), and computed basic statistics over the document set. For STANDARD I used the LLM to produce a summary, keywords, and sentiment for each document (`analyze_document`) and looped over all documents (`process_all_documents`), printing the results directly to the console. The two output helpers (`save_results` and `generate_report`) are left as TODO stubs.

**If you completed BASE:** Stop-word removal used a hard-coded set of common English words (the, a, is, in, of, and, to, for, etc.). Words were lowercased and stripped of punctuation first so they matched the stop-word list reliably. For a production system I would use a more comprehensive list instead of a hand-written set.

**If you completed STANDARD:** The STANDARD pipeline does not currently handle document failures — if `analyze_document` raises (e.g. the LLM returns invalid JSON), the whole `process_all_documents` loop stops.

---

## Process Questions

_These questions are about your experience doing the task, not the code itself._

1. **What did you get stuck on longest?** Describe the specific moment — what you were trying to do, what went wrong, and how you got past it.

Getting back into Python. It was the first language I learned about five years ago, but I'd been mostly working with C++ since(first 2 years of Latvian University Computer science are basically in C++ only), so coming back to it in a short time was rough — everything felt new again. The biggest slowdown was pandas and CSV handling, which I had completely forgotten. I spent a lot of time researching functions to see what already existed — that's how I found `csv.DictReader` instead of parsing files by hand. SQL was easier; I just had to revisit COUNT and JOINs. The hardest tasks were 3 and 4, because the whole LLM/API side was new to me, and task 4 was the hardest since it combined everything into one pipeline. What got me through it was patience: going back to the docs, testing small pieces on their own, and rewriting code into plain steps I could follow line by line.

2. **What did you Google/search for during this task?** List 2–3 specific things you looked up.

I did most of my looking-up through an AI assistant, but I also searched for things like: how to read a CSV in Python (that's where I found `csv.DictReader`), pandas basics to refresh myself on reading and filtering data, and a refresher on SQL COUNT and JOINs since I hadn't used them in a while.

3. **If you used AI tools (Copilot, ChatGPT, etc.), which parts did you use them for?** Be honest — this is not penalized. We want to understand your workflow.

Yes, I used an AI coding assistant for almost everything. I used it to write the code, to explain concepts I didn't understand, and to debug errors. What I tried to do was not just copy the answers: I asked for explanations in simple terms, and I rewrote parts of the code in simpler ways I could actually explain myself. A few functions that came out too advanced for me to confidently explain live, I simplified or removed entirely. I also normally work in C++, especially on my hobby of robotics, so Python was the language I felt least confident in - which is why I leaned on the assistant more here than I usually would. I know I still depend on the assistant a lot, and becoming more independent is the main thing I want to work on.

---

## Self-Estimation

_Rate your current skill level honestly (1 = no experience, 5 = very confident):_

| Skill | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|
| Python programming | [ ] | [ ] | [x] | [ ] | [ ] |
| Working with data (files, CSV, JSON) | [ ] | [ ] | [x] | [ ] | [ ] |
| pandas / data analysis | [ ] | [x] | [ ] | [ ] | [ ] |
| SQL | [ ] | [ ] | [x] | [ ] | [ ] |
| Git and version control | [ ] | [x] | [ ] | [ ] | [ ] |
| REST APIs (calling/building) | [x] | [ ] | [ ] | [ ] | [ ] |
| LLMs and prompt engineering | [ ] | [x] | [ ] | [ ] | [ ] |
| Error handling and debugging | [ ] | [x] | [ ] | [ ] | [ ] |
| Reading documentation to learn new tools | [ ] | [ ] | [x] | [ ] | [ ] |
| Explaining technical concepts to others | [ ] | [x] | [ ] | [ ] | [ ] |

**What is your strongest technical skill overall?**
Persistence and patience. When something doesn't work I keep at it, and I've learned to break a problem into small steps and debug one thing at a time. Years of C++ work also taught me how to figure things out by reading docs and experimenting on my own.

**What is the area you most want to improve during the bootcamp?**
Python and data tooling. I can read and write Python, but I'm slow because I haven't used it in years, and pandas in particular is something I want to get really comfortable with instead of looking everything up.

**Have you built any personal or work projects before? If yes, briefly describe one:**
Yes a bunch, for example, an ESP32 Air Mouse, a Bluetooth PC remote I built as a hobby project. It's an ESP32 microcontroller that reads a motion sensor (MPU6050 accelerometer/gyro), a joystick and buttons, and uses them to control the PC like a wireless mouse. It has three modes selected with a potentiometer: mouse navigation with scrolling and browser shortcuts, media and volume control, and a shutdown timer. The ESP32 firmware is C++ (Arduino), and I wrote a Python script that runs on the PC (using `pynput`, `pyserial` and `pycaw`) to handle the controls and volume over a serial connection, with an OLED screen showing the current mode and status. Building it taught me how software and hardware talk to each other, and it was my first real introduction to Python. https://github.com/justfilips/ESP32-Air-Mouse

---

## Self-Assessment

_What are you least confident about in your submission? What would you do differently next time?_

I'm least confident about exercise 4. I ran out of time before finishing all of STANDARD, and most of the LLM side was new to me, so I was learning a lot in a short window. But it was also the exercise I enjoyed the most, and I'd genuinely like to go back and finish it properly.

Overall I really enjoyed these tasks: loading and cleaning data, writing SQL, and then working with an actual LLM felt very interesting to me. If I did it again, I'd start refreshing Python and pandas earlier and give myself more time, but I came out of this more excited about data and programming than when I started.
