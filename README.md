# RefactorRush
![Application Screenshot](https://raw.githubusercontent.com/wmatecki97/RefactorRush/main/screenshoots/RefactorRush.png)
![Modifications diff](https://raw.githubusercontent.com/wmatecki97/RefactorRush/main/screenshoots/RefactorRush_diff.png)
*results generated with mixtral-8x7b
## Overview

RefactorRush is a powerful tool designed to help developers quickly and easily manage simple technical debt in their projects. Leveraging the capabilities of large language models (LLMs), RefactorRush automates repetitive and time-consuming tasks such as implementing multilanguage support, adding missing logs, and other minor yet essential modifications. This allows you to focus on more complex challenges and accelerate your development process.
Features

* Automated Code Modifications: Select files and let RefactorRush handle the rest, making swift changes across your entire project.
* Technical Debt Management: Efficiently address simple technical debt without manual effort.
* Cost-Effective: Save time and resources by automating routine tasks, enabling you to spend a few cents or dollars on proper logging and other enhancements.
* User-Friendly Interface: Intuitive design that simplifies the process of selecting and modifying project files.
* Focus on Innovation: Free yourself from minor technical tasks to concentrate on testing ideas and achieving your project's full potential.

## Usage

* Select Files: Choose the files you need to modify within your project.
* Specify Changes: Define the type of modifications you want to implement (e.g., add logging, implement multilanguage support).
* Run RefactorRush: Let the tool process the selected files and apply the specified changes automatically.

## Installation

To install RefactorRush, follow these steps:

### Clone the repository
```git clone [https://github.com/yourusername/RefactorRush.git](https://github.com/wmatecki97/RefactorRush)```

### Install dependencies
```pip install -r requirements.txt```

### Run
```python program.py```

## Using custom models
You can use all the models available in langchain LLMs https://python.langchain.com/v0.1/docs/integrations/llms/
To change the model used simply switch the implementation in file_processing.py to set self.llm with LLM of your choice

## Contribution

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/witkor)
