### Artificial Intelligence

---

## **Project Setup**

### **1. Clone the Repository**
Clone the repository to your local machine using the following command:
```bash
git clone <repository-url>
cd <repository-name>
```

---

### **2. Set Up a Virtual Environment**

A virtual environment isolates the project dependencies from the global Python installation.

#### **For Linux/MacOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **For Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see the virtual environment activated (e.g., `(venv)` prefix in your terminal).

---

### **3. Install Project Dependencies**

Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

---

### **4. Verify Installation**

Ensure all dependencies are installed and the environment is set up correctly:
```bash
python -m pip list
```

You should see a list of installed packages matching those in `requirements.txt`.

---

## **Common Commands**

- **Deactivate the Virtual Environment**
  ```bash
  deactivate
  ```

- **Update Dependencies**
  After adding new dependencies, update the `requirements.txt` file:
  ```bash
  pip freeze > requirements.txt
  ```

- **Remove the Virtual Environment**
  If you need to start fresh, delete the `venv` directory:
  ```bash
  rm -rf venv  # Linux/MacOS
  rmdir /s /q venv  # Windows
  ```

---
