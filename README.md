## Getting Started

To run this project, you'll need to set up a virtual environment and install the required dependencies. Here's how:

1. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment:**

    * On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```
    * On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

Now you are ready to run the `gpt_classify.py` script.

You can also select the `venv` as the interpreter in your IDE to ensure that the virtual environment is used for running and debugging the code.

## Using the Classifier

To classify theses using the `gpt_classify.py` script, follow these steps:

1. **Set up your environment variables:**
    - Create a `.env` file in the root directory of the project.
    - Add your OpenAI API key to the `.env` file:
      ```
      OPENAI_API_KEY=your_openai_api_key_here
      ```

2. **Run the classifier script:**
    ```bash
    python gpt_classify.py
    ```

3. **Configuration options:**
    - You can modify the following variables in the `gpt_classify.py` script to customize the classification process:
      - `MODEL_NAME`: Choose between 'gpt-4o' and 'gpt-4o-mini'.
      - `SUBSET_SIZE`: Number of theses to classify. Set to 1000 for all theses.
      - `CLASSIFICATION_METHOD`: Choose between 'accuracy' and 'cost'.
      - `DATASET_PATH`: Choose between 'thesis_records_train.csv' and 'thesis_records_test.csv'.
      - `CATEGORY_BOOK_PATH`: Path to your category book CSV file.

The classification results will be saved in a CSV file with a timestamp in the filename.