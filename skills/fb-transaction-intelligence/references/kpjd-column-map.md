# KPJD Excel Column Mapping

## Sheet Name Pattern
- `Trans_YYYYMMDD` (e.g., `Trans_20260808`)

## Column Index (0-based)

| Index | Column Name | Description |
|-------|-------------|-------------|
| 0 | No | Row number |
| 1 | Date | Transaction date/time (M/D/YYYY HH:MM:SS AM/PM) |
| 2 | Reference No | Unique reference number |
| 3 | MerchantCode | Merchant identifier (e.g., M46098) |
| 4 | Merchant Name | Business name (e.g., "WebOfProjects-VM(Cheras)") |
| 5 | TransId | Transaction ID from payment processor |
| 6 | AuthCode | Authorization code (may be empty for QR) |
| 7 | CreditCard Name | Card holder name (empty for QR payments) |
| 8 | CreditCard No | Masked card number (empty for QR) |
| 9 | CreditCard Bank | Issuing bank (empty for QR) |
| 10 | CreditCard Country | Card country (empty for QR) |
| 11 | CreditCard Type | Card type (empty for QR) |
| 12 | Payment Method | `DuitNow QR`, `TNG QR (MYR)`, `GrabPay QR` |
| 13 | Payment Category | Sub-category (e.g., `GPWALLET` for GrabPay) |
| 14 | Card Type | Further classification |
| 15 | Currency | Always `MYR` for Malaysian transactions |
| 16 | Amount | Transaction amount in MYR |
| 17 | Discount | Discount applied (usually 0.0) |
| 18 | ProdDesc | Product description (food/drink item name) |
| 19 | User Email | Customer email (masked) |
| 20 | User Contact | Customer phone (masked) |
| 21 | Country | Usually `RESERVED` |
| 22 | IpAddress | Terminal IP (e.g., `10.1.0.37`) |
| 23 | Remark | Additional notes |
| 24 | TerminalID | Terminal identifier |
| 25 | Status | `Success` or error description |

## Payment Method Values

| Value | Description |
|-------|-------------|
| `DuitNow QR` | DuitNow QR code payment |
| `TNG QR (MYR)` | Touch 'n Go QR payment |
| `GrabPay QR` | GrabPay wallet payment |

## Common Product Descriptions (F&B)

Based on KPJD exports from burger/F&B stalls:
- Burgers: BURGER BUTTERMILK CH, BURGER BLACK PEPPER, BURGER CHEESE CHICKE, BURGER SPICY CHICKEN
- Sandwiches: SANDWICH TUNA, SANDWICH EGG, SANDWICH CURRY CHICK
- Drinks: MILO, CHOCOLATE MILK, STRAWBERRY MILK, ZUS LATTE, ZUS BOSS BLEND
- Snacks: CHOCO ROLLS MUZIC, HONEY ROASTED CASHEW, SPRITzer MINERAL WAT, DRINHO LEMON SPARKLI
