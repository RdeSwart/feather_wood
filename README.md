# Feather and Wood

Feather and Wood is a website that sells wooden, plush and STEM toys to those who want to engage their children in toys and games that don't have the hyper stimulation that plastic, battery toys tend to have.
Alot of these customers follow or are curious about the Montessorri or Steiner teachings, which is ultimately teaching through play, giving space for the individual child's own imagination.

![Am I responsive image]()
![Click here to view the live site]()

## Table of Contents:

1. [User Experience(UX)](#user-experience)
   _[Strategy / Site Goals](#strategy-site-goals)
   _[Scope / User Stories](#scope-user-stories)
   _[Structure / Design](#structure-design)
   _[Colour Scheme](#colour-scheme)
   _[Fonts Used](#fonts-used)
   _[Wireframes](#wireframes)
   _[Database Schema](#database-schema)
   _[Agile Methodology](#agile-methodology)
2. [Features](#features)
3. [Marketing](#marketing)
4. [SEO](#seo)
5. [Testing](#testing)
6. [Bugs](#bugs)
7. [Technologies and Languages](#technologies-and-languages)
8. [Deployment](#deployment)
   _[Cloning](#cloning)
   _[Forking](#forking)
9. [Credits](#credits)

## User Experience

### <ins>Strategy / Site Goals:</ins>

As a B2C(Business to Consumer) website, our goal is to create an easy-to-use, intuitive site that gives the consumer a great shopping experience. With features such as an easy payment gateway, a trusted authentication system, a search
and filter feature, high quality images, clear product descriptions, a ratings/review feature, a shopping cart overview, being just some, we are confident we will meet the ultimate goal for our users, consumers and owners alike.

### <ins>Scope / User Stories:</ins>

#### As a customer, I want to...:

1. Be able to see this is the right website for me by the HomePage. It will be clear as to it's purpose from the first time I visit it.
2. Be able to see products available and click into them for more information
3. Be able to clearly see a price and a reduction in price if it is on sale.
4. Be able to visit the Page's About Me section to see if the company's goals and ethics are similar to my own.
5. Be able to make a purchase without having to register as a user first.
6. Be able to search for a certain product that I know by name.
7. Be able to view what is in my cart.
8. Be able to edit my cart to either increase or decrease a quantity.
9. Be able to delete my cart or certain items in my cart.
10. Be able to enter my payment info, with the knowledge it is a trusted site.
11. Be able to view my order confirmation after I have checked out.
12. Be able to recieve an order confirmation email.
13. Be able to register for an account
14. Be able to login / logout easily.
15. Be able to recover my password if I forget it.
16. Be able to have a personalised user profile, where I can see my past orders.

#### As a site owner/Admin, I want to...:

1. Be able to have an overview of all models on the site.
2. Be able to have full CRUD functionality for products, sales etc
3. Be able to see orders and customer details.

<details><summary>Click to view KanBan</summary>

![Image of KanBan]()

</details>

### <ins>Structure / Design:</ins>

#### Colour Scheme:

Talk of colour scheme here........................

#### Fonts Used:

Talk of Google fonts here........................

#### Wireframes:

I used Balsamiq to create the wireframe for the project.

<details><summary>Click to view Wireframes</summary>

![Wireframe desktop]()
![Wireframe mobile]()

</details>

#### Database Schemas:

##### <ins>User Model</ins>

As part of the Django built-in AllAuth library, this model holds information about the User.

- id: PrimaryKey
- username: CharField
- password: Charfield
- email: EmailField
- is_superuser: BooleanField

##### <ins>Product Model</ins>

The Product Model object represents the products on sale, created by the SuperUser. It consists of the following fields:

- id: PrimaryKey
- name: Charfield
- category: ForeignKey
- brand: ForeignKey
- price: DecimalField
- sale_price: DecimalField
- details: TextField
- description: CharField
- rating: DecimalField
- discount: DecimalField
- image_url: UrlField
- image: ImageField

##### <ins>User Profile Model</ins>

- id: PrimaryKey
- user: OneToOne
- default_phone_number: CharField
- default_street_address1: CharField
- default_street_address2: CharField
- default_town_or_city: CharField
- default_county: CharField
- default_postcode: CharField
- default_country: CountryField

##### <ins>Order Model</ins>

- id: PrimaryKey
- order_number: CharField
- user_profile: ForeignKey
- full_name: CharField
- email: EmailField
- phone_number: CharField
- street_address1: CharField
- street_address2: CharField
- town_or_city: CharField
- county: CharField
- postcode: CharField
- country: CountryField
- date: DateTimeField
- delivery_cost: DecimalField
- order_total: DecimalField
- grand_total: DecimalField

##### <ins>Order Line Item Model</ins>

- id: PrimaryKey
- order: ForeignKey
- product: ForeignKey
- quantity: IntegerField
- lineitem_total: DecimalField

##### <ins>Category Model</ins>

- id: PrimaryKey
- name: Charfield
- friendly_name: CharField

##### <ins>Review Model</ins>

- id: PrimaryKey
- user_profile: ForeignKey
- product: ForeignKey
- product_rating: IntegerField
- title: CharField
- user_review : TextField
- date_created: DateTimeField

##### <ins>Wishlist Model</ins>

- id: PrimaryKey
- user_profile: ForeignKey
- product: ManyToMany

##### <ins>Brand Model</ins>

- id: PrimaryKey
- name: Charfield
- friendly_name: CharField
- image_url: UrlField
- image: ImageField

<details><summary>Click to view ERD</summary>

![Image of ERD]()

</details>

#### Agile Methodology: THIS NEEDS MORE WORK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Adopting the Agile method for this project, I was able to break down the huge and overwhelming feat of the tasks it would take to get
this project, not only off the ground but as an up and running working software solution!
By breaking down the tasks into increments, I was easily able to modify or add as needed.

Starting with basic User Stories, I was able to break these down into Epics and then Sprints.

##### <ins>Epic 1:</ins>

Related to User Stories: #

#####Sprint 1:
Create the site's basic structure and functionality

Tasks:

1. Create Django project and basic folder structure
2. Set up User Authentication with AllAuth
3. Create Database models for Products, Users and Orders
4. Create a Product Detail Template with Bootstrap

##### <ins>Epic 2:</ins>

Related to User Stories: #

#####Sprint 2:
Implement CRUD functionality and expand on website features

Tasks:

1. Implement CRUD for Admin on products, categories etc
2. Create a shopping bag for adding, editing and removing items(order and OrderLineItem)
3. Install Stripe API to use for secure payments

##### <ins>Epic 3:</ins>

Related to User Stories: #

#####Sprint 3:
Focus on UX(User Experience) by adding extra features to the site

Tasks:

1. Create a Search Bar to search for brands, products etc
2. Create a Review model, so users can review items they have bought.
3. Create a Wishlist model, so users can add products to their wishlist once they are registered.
4. Create a Brand Model, so users can search by well-known manufacturer titles.

##### <ins>Epic 4:</ins>

Related to User Stories: #

#####Sprint 4:
Test all features manually, push final deploy and finish any documentation

Tasks:

1. Test all features once finally deployed
2. Fix and document any bugs
3. Note testing in docs

## Features:

1. Navbar
<details><summary>Click to view NavBar</summary>

![Image of NavBar]()

</details>

2. Toasts
<details><summary>Click to view Toasts</summary>

![Image of Toast]()

</details>

3. Breadcrumbs
<details><summary>Click to view Breadcrumbs</summary>

![Image of Breadcrumbs]()

</details>

4. Footer
<details><summary>Click to view Footer</summary>

![Image of Footer]()

</details>

3. Home Page
<details><summary>Click to view Home Page</summary>

![Image of Home Page]()

</details>

    * Hero Section
    <details><summary>Click to view Hero Section</summary>

    ![Image of Hero Section]()

    </details>

    * Featured Products
    <details><summary>Click to view Featured Products</summary>

    ![Image of Featured Products]()

    </details>

- Newsletter Signup
<details><summary>Click to view Newsletter Signup</summary>


    ![Image of Newsletter Signup]()

    </details>

4. Product Page
<details><summary>Click to view Product Page</summary>

![Image of Product Page]()

</details>

- Single Product Card
<details><summary>Click to view Single Product Card</summary>


    ![Image of Single Product Card]()

    </details>

- Page Pagination
<details><summary>Click to view Page Pagination</summary>


    ![Image of Page Pagination]()

    </details>

5. Product Details Page
<details><summary>Click to view Product Details Page</summary>

![Image of Product Details Page]()

</details>

- Review Product - Create
<details><summary>Click to view Review Product - Create</summary>


    ![Image of Review Product - Create]()

    </details>

- Review Product - Edit
<details><summary>Click to view Review Product - Edit</summary>


    ![Image of Review Product - Edit]()

    </details>

- Review Product - Delete
<details><summary>Click to view Review Product - Delete</summary>


    ![Image of Review Product - Delete]()

    </details>

6. About Page
<details><summary>Click to view About Page</summary>

![Image of Product About Page]()

</details>

7. Brands Page
<details><summary>Click to view Brands Page</summary>

![Image of Product Brands Page]()

</details>

8. User Profile Page
<details><summary>Click to view User Profile Page</summary>

![Image of User Profile Page]()

</details>

9. Shopping Bag Page
<details><summary>Click to view Shopping Bag Page</summary>

![Image of User Shopping Bag Page]()

</details>

10. Checkout Page
<details><summary>Click to view Checkout Page</summary>

![Image of User Checkout Page]()

</details>

11. Order Confirmation Page
<details><summary>Click to view Order Confirmation Page</summary>

![Image of Order Confirmation Page]()

</details>

12. Order Confirmation Email
<details><summary>Click to view Order Confirmation Email</summary>

![Image of Order Confirmation Email]()

</details>

13. Administration Page Overview
<details><summary>Click to view Administration Page Overview</summary>

![Image of Administration Page Overview]()

</details>

### Future Features:

## Marketing:

## SEO:

## Testing:

## Bugs:

## Technologies and Languages:

## Deployment:

### Cloning:

### Forking:

## Credits:
