# **Departments and Employees**

## **Vision**

“Departments and Employees” is web-application which allows users to record information about departments and their employees.

Application should provide:

-   Storing departments and employees in database;
-   Displaying list of departments;
-   Displaying list of employees;
-   Updating the list of departments (adding, editing, removing);
-   Updating the list of employees (adding, editing, removing);
-   Possibility to search for employees based on their birthday or if their were born in a specific period;
-   Filtering departments by the average salary;

## **Departments**

### **1.1 Display list of departments**

The mode is designed to view the list of departments.

***Main scenario:***

-   User selects item “Departments”;
-   Application displays the list of departments;

![Image of the departments page](./mockup_imgs/depart_page.png)

Pic 1.1 view of the Department list

The list displays the following columns:

-   Department ID – unique department number
-   Department name – human-understandable unique department name
-   Number of employees – the number of employees in the department
-   Average salary – the average salary of the departments

Aggregate function: Average salary = SUM(Emloyees.employee\_salary) / Number of employees

Filtering by the average salary:

-   User chooses a comparison operator (&lt;, &gt;, =, &lt;=, &gt;=), enters the average salary and the app filter the table;

### **1.2 Add Department**

***Main scenario:***

-   User clicks the “Add” button on the Departments page;
-   Application displays the form for adding department;
-   User enters department data and clicks “Save” button;
-   If any data is entered incorrectly, incorrect data message is displayed;
-   If entered data is valid, then the record is added to the database;
-   If an error occurs, then the error message is displayed;
-   If the record is added successfully, then User gets redirected to the Departments page;

***Cancel operation scenario:***

-   User clicks the “Add” button on the Departments page;
-   Application displays the form for adding department;
-   User enters department data and clicks “Cancel” button;
-   Data doesn’t save to the database and the user is redirected to the Departments page;
-   If the user selects Departments or Employees from the menu, then the data won’t be saved in the database and the corresponding page will open;

![Image of the add department page](./mockup_imgs/edit_page.png)

Pic 1.2 Add department

When adding a department, the following details are entered:

-   Department’s name – the name of the departments;

### **1.3 Edit Department**

***Main scenario:***

-   User clicks the “Edit” button on the Departments page;
-   Application displays form with current Department’s data;
-   User edits the department’s data and clicks “Save”;
-   If any data is entered incorrectly, the incorrect data message is displayed;
-   If entered data is valid, then the change is saved to the database;
-   If error occurs, the error message is displayed;
-   If the change is saved successfully, then the use is redirected to the departments page;

Cancel operation scenario:

-   User clicks the “Edit” button on the Departments page;
-   Application displays form with current Department’s data;
-   User edits the department’s data and clicks “Cancel”;
-   Data doesn’t save to the database and the user is redirected back to the Departments page;
-   If the user selects Departments or Employees from the menu, then the data won’t be saved in the database and the corresponding page will open;

![Image of the edit department page](./mockup_imgs/edit_page.png)

Pic 1.3 Edit department

When editing a department, the following data can be changed:

-   Department’s name – the name of the department;

### **1.4 Removing a Department**

***Main scenario:***

-   User clicks the “Remove” button in the corresponding line;
-   Then the prompt appears asking the use to confirm removal;
-   The user confirms the removal;
-   The recorded is deleted from the database;
-   If error occurs, the error message is displayed;
-   If record removal went successfully, then the Departments page is displayed without the deleted record;

![Image of the delete department prompt](./mockup_imgs/delete_prompt.png)

Pic 1.4 Remove department

***Cancel operation scenario:***

-   User clicks the “Remove” button in the corresponding line;
-   Then the prompt appears asking the use to confirm removal;
-   The user cancels the removal;
-   The Departments page is displayed without any changes;
