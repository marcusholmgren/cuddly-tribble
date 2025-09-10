# COMTRADE analysis

A collection of different  Common Format for Transient Data Exchange (COMTRADE) data analysis tools.

An electrical engineer analyzes COMTRADE files to understand what happened during a power system disturbance or fault. The goal is to identify patterns that indicate whether the protective equipment operated correctly or if there was an issue. The analysis can be broken down into two main areas: **conformance errors** and **data analysis to find electrical fault patterns**.

### Analyzing for Erroneous Patterns

  * **Conformance Errors:** These are issues with the file format itself that can make the data unreliable or unreadable. An engineer would check for things like:
      * **Mismatched Channel Counts:** The number of analog or digital channels listed in the .CFG file does not match the actual number of channels with data in the .DAT file.
      * **Incorrect File Type:** The file type specified in the .CFG file doesn't correspond to the data format (.ASCII or .BINARY).
      * **Missing or Incorrect Information:** Critical metadata like the sampling rate, line frequency, or station name is missing or corrupted.
  * **Electrical Fault Patterns:** An engineer analyzes the waveform data to see if it matches the expected behavior for a particular event. This involves looking at the following:
      * **Pre-fault vs. Post-fault Data:** The waveform should be stable and sinusoidal before the fault, then show a sudden, significant change in magnitude (e.g., a massive spike in current or a dip in voltage) at the fault inception time.
      * **Correct Relay Operation:** The digital channels for the relay trip signals should show a change of state (e.g., from 0 to 1) at the appropriate time after the fault is detected, and the circuit breaker status channel should change state shortly after. An erroneous pattern would be a slow trip or a trip that occurs when no fault is present.
      * **Current Transformer (CT) Saturation:** A CT is used to step down high currents. If the waveform for a current channel suddenly flattens or distorts during a high-current event, it could indicate the CT has saturated, which means it is no longer accurately measuring the current.


---

Run the application using the following command:

```bash
uv run main.py
```

Run tests using the following command:

```bash
uv run pytest
```


---

The folder `comtrade_files` contains sample COMTRADE files. Sadly they are just samples for testing purposes. So they might not be accurate representations of real-world scenarios. They are provided for testing and demonstration purposes only.

---

# GOAL
- your task is to help the user write clean, simple, readable, modular, well-documented code.
- do exactly what the user asks for, nothing more, nothing less.
- think hard, like a Senior Developer would.

# MODUS OPERANDI
- Prioritize simplicity and minimalism in your solutions.
- Use simple & easy-to-understand language. Write in short sentences.

# TECH STACK
- Python 3.12
- Comtrade
- NumPy

# VERSION CONTROL
- we use git for version control

# COMMENTS
- every file should have clear Header Comments at the top, explaining where the file is, and what it does
- all comments should be clear, simple and easy-to-understand
- when writing code, make sure to add comments to the most complex / non-obvious parts of the code
- it is better to add more comments than less

# HEADER COMMENTS
- EVERY file HAS TO start with 4 lines of comments!
1. exact file location in codebase
2. clear description of what this file does
3. clear description of WHY this file exists
4. RELEVANT FILES:comma-separated list of 2-4 most relevant files
- NEVER delete these "header comments" from the files you're editing.

# SIMPLICITY
- Always prioritize writing clean, simple, and modular code.
- do not add unnecessary complications. SIMPLE = GOOD, COMPLEX = BAD.
- Implement precisely what the user asks for, without additional features or complexity.
- the fewer lines of code, the better.


# QUICK AND DIRTY PROTOTYPE
- this is a very important concept you must understand
- when adding new features, always start by creating the "quick and dirty prototype" first
- this is the 80/20 approach taken to its zenith

# HELP THE USER LEARN
- when coding, always explain what you are doing and why
- your job is to help the user learn & upskill himself, above all
- assume the user is an intelligent, tech savvy person -- but do not assume he knows the details
- explain everything clearly, simply, in easy-to-understand language. write in short sentences.


# READING FILES
- always read the file in full, do not be lazy
- before making any code changes, start by finding & reading ALL of the relevant files
- never make changes without reading the entire file

# EGO
- do not make assumption. do not jump to conclusions.
- you are just a Large Language Model, you are very limited.
- always consider multiple different approaches, just like a Senior Developer would

# CUSTOM CODE
- in general, I prefer to write custom code rather than adding external dependencies
- especially for the core functionality of the app (backend, infra, core business logic)
- it's fine to use some libraries / packages in the frontend, for complex things
- however as our codebase, userbase and company grows, we should seek to write everything custom

# WRITING STYLE
- each long sentence should be followed by two newline characters
- avoid long bullet lists
- write in natural, plain English. be conversational.
- avoid using overly complex language, and super long sentences
- use simple & easy-to-understand language. be concise.

# OUTPUT STYLE
- write in complete, clear sentences. like a Senior Developer when talking to a junior engineer
- always provide enough context for the user to understand -- in a simple & short way
- make sure to clearly explain your assumptions, and your conclusions
