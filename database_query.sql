-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Budgets table
CREATE TABLE budgets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT NOT NULL,
    client_name TEXT NOT NULL,
    annual_budget DECIMAL(15,2) NOT NULL,
    reduced_budget DECIMAL(15,2),
    budget_received_date TIMESTAMP WITH TIME ZONE,
    budget_from TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Expenses table
CREATE TABLE expenses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT NOT NULL,
    budget_id UUID REFERENCES budgets(id) ON DELETE CASCADE,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    comment TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Payroll', 'Mileage', 'Extras', 'Host Fee')),
    cost DECIMAL(15,2) NOT NULL,
    gst_status TEXT NOT NULL CHECK (gst_status IN ('Inc', 'Excl')),
    total DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create indexes for better performance
CREATE INDEX idx_budgets_user_id ON budgets(user_id);
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_expenses_budget_id ON expenses(budget_id);
CREATE INDEX idx_expenses_date ON expenses(date);

-- Row Level Security (RLS)
ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can only access their own budgets" ON budgets
    FOR ALL USING (auth.uid()::text = user_id);

CREATE POLICY "Users can only access their own expenses" ON expenses
    FOR ALL USING (auth.uid()::text = user_id);