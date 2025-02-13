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

## Output Format

The classification results will be saved in a CSV file with a timestamp in the filename. The CSV file will contain the following columns:

- `Link`: The link to the thesis.
- `Category1`, `Category2`, ...: Columns for each category from the category book, with values 1 (true) or 0 (false) indicating whether the category applies to the thesis.

Example:

```
Link,Net-Net Asset Plays,Excess Cash Bargain,...
http://example.com/thesis1,1,0,...
http://example.com/thesis2,0,1,...
```

## Category Book Format

The category book CSV file should have the following columns:

- `Label`: The name of the investment category.
- `Description`: A brief description of the investment category.
- `Method`: The method used to identify the category in the thesis. (Not used in this script)

Example:

```
Label,Description,Method
Net-Net Asset Plays,Buy firms trading below net current asset value (NCAV).,"Filter for Price < (Current Assets – Total Liabilities), ensuring basic business viability."
Excess Cash Bargain,Focus on companies whose cash exceeds their market cap.,Screen for negative enterprise value; check that core operations are at least stable.