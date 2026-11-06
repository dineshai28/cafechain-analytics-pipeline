
```mermaid
erDiagram
    dim_stores ||--o{ fact_sales : "store_id"
    dim_products ||--o{ fact_sales : "product_id"
    dim_employees ||--o{ fact_sales : "employee_id"

    dim_stores {
        int store_id PK
        string store_name
        string city
        string region
    }

    dim_products {
        int product_id PK
        string product_name
        string category
        float cost_price
    }

    dim_employees {
        int employee_id PK
        string employee_name
        string role
    }

    fact_sales {
        int order_id PK
        int store_id FK
        int product_id FK
        int employee_id FK
        float quantity
        float unit_price
        timestamp order_date
    }
