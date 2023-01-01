# use corresponding placehodler account when read words
asset_use_account = {
    "income": [
        "Interest received",
        "Interest",
        "payroll",
    ],
    "assets": [
        "transfer to",
        "transfer from"
    ],
    "liabilities": [
        "payment to"
    ]
}

# use cash flow sign when read words
asset_cash_flow = {
    "-": [
        "e-Transfer sent",
        "Payment",
        "to"
    ],
    "+": [
        "Payroll Deposit",
        "from",
        "Interest",
    ]
}

# use cash flow sign + when read words
liability_cash_flow_in = {
    "+": [
        "PAYMENT - THANK YOU",
        "PAYMENT THANK YOU",
        "PAYMENT RECEIVED"
    ]
}
