# Scrape and Stream

## Overview

This project is a web application that allows users to scrape data and stream it efficiently.

## Prerequisites

- Python 3.x
- Node.js
- npm

## Getting Started

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

First, clone the repository using the following command:

```bash
git clone https://github.com/Mike-Medvedev/scrape-and-stream.git
```
2. Set Up a Virtual Environment
Navigate to the root directory of the cloned repository:

```bash
cd scrape-and-stream
```

Then, create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the Virtual Environment
Change into the virtual environment directory and activate it:

```bash
cd venv
source bin/activate
```

4. Set Up the Backend
Once the virtual environment is activated, navigate to the backend directory:

```bash
cd backend
```
Now, install the required Python packages:

```bash

pip install -r requirements.txt
```
5. Run the Backend Server
After installing the requirements, you can run the FastAPI development server:

```bash

fastapi dev --port=5000
```
6. Set Up the Frontend
Now, back out of the backend directory:

```bash

cd ..
```
Then, navigate to the scrapr-ui directory and install the necessary Node.js packages:

```bash

cd scrapr-ui
npm install
```

7. Run the scrapr-ui Development Server
Finally, you can run the scrapr-ui application with the following command:

```bash

npm run dev
```
