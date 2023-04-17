# DataScienceGPT

DataScienceGPT (bigger and better name coming soon) will be a Python app that uses AI to perform useful analysis on a user provided data set. Harnessing OpenAI's large language model GPT-3.5, the app will hopefully be really simple to use, even for a non-specialist! Below is a basic outline of the workflow:

1. The user uploads their data (.csv file) and provides a task to the app.
2. The header of the data file is extracted and the task is turned into a prompt.
3. The header and prompt are then inserted into an API call to OpenAI which will
    * Produce python code to achieve the task, possibly providing an explanation of the code,
    * Run the code,
    * Provide the user with the output (this could be a figure, table, number etc.), and an interpretation.
4. At this point the user could leave a happy chappy, or if the task is not fulfilled to their liking, they can provide feedback. The app will use this feedback to edit the prompt in step 2, and the re-run step 3.
