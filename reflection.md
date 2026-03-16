# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

The first time I ran the game, it was almost unplayable. At first sight it looks good, but its flaws are revealed through playing. My approach was doing a binary search but because the hints are flipped it was incorrect. The Score calculation is also confusing and not clear. The secret kept changing.
The new game button did not restart the game, it only changed the value of the secret. The hints are flipped, so lower was displayed when the user had to go higher. Changing the difficulty only changed how many attempts you had. The game would end even if you had 1 attempt left. The debug history doesn't update after each submission, it is delayed by 1 attempt (registers attempt 2 only after running attempt 3). The instructions for the range of numbers to guess don't change with settings changes. The game counts invalid input as attempts and doesn't consider out of range integers as invalid input. Finally, when NOT guessing the secret in your first attempt, you have to click the submit button twice to register it.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Windsurf explain, claude code.

A correct suggestion for solving hints not working properly that claude provided was to swap the hint messages in both the numeric path (lines 38-40) and the string-comparison fallback. I verified by running an instance of the game where I guess lower and then higher  multiple times with hints enabled to check for correct and consistent output.

An incorrect suggestions was fixing the new game button. The applied fix by claude did not solve the issue and had to be revised. It only solved it partially as it now works when the user is not at an end screen (win/lose screen) and clicks it during a session. The ai suggested "new_game only resets secret and attempts, but leaves stauts, history, and score untouched. Since status stays "won" or "lost", the game hits st.stop() on line 145 immediately after rerun — making it appear frozen." I tested the button again and then reprompted claude with more detailed instructions, which lead it to identify the same issue in more detail and fixing the hardcoded random.randint(1, 100).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed after running iterations of the game and testing the features in a Quality Assurance way. I tested the fixes to see if the feature behaved as expected or not and tested edge cases.
I ran multiple tests, one test was using pytest to check if new game resets after winning. It showed the button was working properly and reseting the state accordingly. 
AI helped me check for syntax and understand how the test worked. I used windsurf explain for this.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

Secret changed because of two reasons: Streamlit reruns overwriting it after interactions and a block of code ran on every submit that changed what value passed to check_guess on alternating attempts. The issue was about the data type changing not the number.
Every time a user interacts with anything on the page, Streamlit re-runs the entire app.py file from top to bottom. Its like refreshing a webpage on every interaction. This resets values like score that were stored in the file, never accumulating. st.session_state (session state) is a dictionary that Streamlit keeps alive between reruns as long as the browser tab is open. So all important game values are stored there to keep them from reseting.
I ensured the session_state guard was properly implemented, fixed the hardcoded random.randint, and removed the odd/even type-switching block so that check_guess always recieves the secret as an int.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Giving the AI a starting point and asking it to run diagnostics on the feature to fix. Then asking for possible fixes and trying them out, keeping a feedback loop.
- What is one thing you would do differently next time you work with AI on a coding task?
Give longer prompts in some cases and optimize token usage. Maybe use more claude code features.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
It shows that AI can falsely determine when a project is production ready and that we have to be careful and run thorough e2e tests and QA tests to ensure the app works properly. AI is good at giving a skeleton or unfinished product.
