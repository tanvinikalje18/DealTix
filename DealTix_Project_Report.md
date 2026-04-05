# DealTix Project Report (Blackbook)

## 1. Introduction
**DealTix** is a comprehensive event ticketing and reselling marketplace designed to help users discover events, book tickets, and resell their existing tickets securely. Unlike traditional ticketing systems, DealTix implements an integrated secondary marketplace where verified users can negotiate prices, verify ticket authenticity, and complete transactions securely under one platform. 

## 2. Problem Statement
The secondary market for event tickets is often plagued by scalping, counterfeit tickets, and untrustworthy communication channels. Buyers face a high risk of fraud when purchasing tickets from individuals on unverified platforms. Furthermore, sellers often struggle to find genuine buyers in a safe environment.

## 3. Proposed Solution
DealTix solves these issues by offering an integrated ticket reselling ecosystem that includes:
- **Direct in-app messaging** for buyer-seller negotiation, reducing reliance on third-party channels.
- **Proof of authenticity** where sellers must attach an authentication image of their ticket before listing.
- **Secure payment gateways** for transaction handling, keeping funds safe until delivery is arranged.
- **Seller rating and review system** to build a community of trusted sellers.

## 4. Technology Stack
The application is structured using a robust backend framework and a modern, utility-first frontend aesthetic.
* **Programming Language**: Python 3.x
* **Web Framework**: Django 6.0
* **Frontend Design**: HTML5, Vanilla CSS, Tailwind CSS Integration (Utility classes for responsive layouts)
* **Database Management System (DBMS)**: SQLite (SQLite3) for development/test databases.
* **Payment Integration**: Razorpay API for handling ticket transactions.

## 5. System Architecture
DealTix uses the MVC (Model-View-Controller) architecture—commonly referred to in Django as MVT (Model-View-Template).

### Key Modules and Models
1. **User Auth & Profiles**: Built on top of Django's native authentication (`User`), extended with a `UserProfile` model handling full name, phone number, and verification status.
2. **Events & Categories**: The `Event` and `Category` models store primary event details such as title, date, location, original price, and total available tickets.
3. **Ticket Marketplace (`TicketListing`)**: Tracks tickets listed by individual sellers allowing specifications on `ticket_type`, `quantity`, `price_per_ticket`, and requiring an `authentication_image`.
4. **Orders & Payments (`Order`, `Payment`)**: Secure checkout storing the overall order, tracking `tickets_bought`, `delivery_address`, and integrating `Razorpay` payment credentials per transaction.
5. **Chat System (`Message`)**: Provides one-to-one communication linking a `sender`, `receiver`, and the specific `TicketListing` being negotiated.
6. **Reviews (`Review`)**: Post-transaction rating system allowing buyers to rate their seller.

## 6. Key Features
- **Event Discovery:** Filter and search events efficiently.
- **Selling Flow:** Users can list a ticket with proof, tracking listed quantity vs total available.
- **In-App Messaging:** Real-time negotiation via the Inbox and Chat portals.
- **Secure Processing:** Buying tickets processes a mock Razorpay window ensuring checkout integrity.
- **Dynamic Updates:** Tickets that are actively being brokered update the 'Marketplace Tickets' properties dynamically.

## 7. Conclusion
DealTix bridges the gap between primary event ticketing and secondary reselling. By emphasizing security features like image authentication and peer review systems, the platform minimizes ticket fraud while maximizing access to sold-out events.

---
*Generated for Project Documentation / Blackbook References*
