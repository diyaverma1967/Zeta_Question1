# Dispute Risk Classification API

## Overview
The Dispute Risk Classification API helps predict the risk level of disputes in financial transactions. It uses machine learning to classify disputes as High or Low risk, assigns a priority level, and suggests a recommended action. This helps businesses automate decision-making and manage disputes more efficiently.

## How It Works
1. **Dispute Data**: A client sends dispute details to the API.
2. **Model Prediction**: The API runs a pre-trained model to predict whether the dispute is high or low risk.
3. **Business Rules**: Based on the prediction, priority and action are assigned using business rules.
4. **Response**: The API returns the risk classification, priority, and recommended action.

## Request & Response Fields

| **Field Name**        | **Type**         | **Description**                                                     | **Example**                | **Request/Response** |
|-----------------------|------------------|---------------------------------------------------------------------|----------------------------|----------------------|
| `transaction_amount`  | float            | The amount of the disputed transaction                              | 150.0                      | Request              |
| `customer_age`        | integer          | Age of the customer                                                | 35                         | Request              |
| `customer_tenure`     | integer          | Number of months the customer has been with the bank               | 24                         | Request              |
| `account_type`        | string           | Type of the customer's account                                      | "premium", "standard"      | Request              |
| `dispute_reason`      | string           | The reason for the dispute                                          | "unauthorized_transaction" | Request              |
| `channel`             | string           | The channel through which the dispute was made                      | "mobile", "web"            | Request              |
| `customer_flagged`    | binary (0 or 1)  | Whether the customer has been flagged for suspicious activity       | 0                          | Request              |
| `previous_disputes`   | integer          | Number of previous disputes by the same customer                    | 1                          | Request              |
| `dispute_time`        | datetime         | Date and time of the dispute (ISO 8601 format)                      | "2023-05-15T14:30:00"      | Request              |
| `risk`                | string           | The predicted risk level                                            | "High", "Low"              | Response             |
| `priority`            | string           | The priority level assigned to the dispute                          | "High", "Medium", "Low"    | Response             |
| `recommended_action`  | string           | The action suggested for the dispute (e.g., "Investigate")          | "Investigate"              | Response             |

## Error Handling

| **Error Code**         | **Description**                                           |
|------------------------|-----------------------------------------------------------|
| `400 Bad Request`      | Invalid input data (FastAPI automatically handles this). |
| `500 Internal Server Error` | Something went wrong with processing the request. |

## Model Expectations

The model expects the following input data in **exact format**:

| **Field Name**        | **Type**         | **Description**                                                     |
|-----------------------|------------------|---------------------------------------------------------------------|
| `transaction_amount`  | float            | Amount of disputed transaction                                      |
| `customer_age`        | integer          | Age of the customer                                                |
| `customer_tenure`     | integer          | Number of months customer has been with the bank                    |
| `account_type`        | string           | Type of account ("premium", "standard")                             |
| `dispute_reason`      | string           | Reason for the dispute                                             |
| `channel`             | string           | Channel where the dispute was initiated                             |
| `customer_flagged`    | binary (0 or 1)  | Whether 1 or 0

## Request Body
<img width="1407" alt="Screenshot 2025-04-30 at 10 22 02ΓÇ»PM" src="https://github.com/user-attachments/assets/fdf916fd-536e-4360-a58a-6a798736a7e0" />

## Response Body
<img width="563" alt="Screenshot 2025-04-30 at 10 28 29ΓÇ»PM" src="https://github.com/user-attachments/assets/cd754502-6409-49ef-a5a2-9c7a2fc1e4cb" />
