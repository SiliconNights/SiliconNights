## SCRUM Meetings
#### [Scrum Meetings](https://docs.google.com/spreadsheets/d/1V9OtsbMmw0wnypaUizGiNEG1rD8Z_nNtrYLTDAiGpLY/edit?usp=sharing)

Silicon Nights
==============

Software Requirements Specifications Sheet
==========================================

**CS 480 Winder 2018**

**Baldemar Sepulveda**

**Brian Bauer**

**Rafael Salinas**

**Saif Aljashamy**

**
**

Introduction
------------

At Silicon Nights we aim to deliver a quality product for the client,
Edwin Rodriguez. We are tasked in creating a web service that will be
used as a repository for recipes that are created by users of the site.
We aim to get this web service complete as quickly as possible and for
the client to be as satisfied as possible with the final product.

*Problem Description*
---------------------

-   A website/web-application needs to be made and it needs to be easily
    accessible.

-   There needs to be a data base containing all the recipes and all the
    users along with any relevant data that the users and/or the recipes
    require, for instance a list of ingredients.

-   There needs to be a functional user sign in and registration system.

-   There also needs to be a way for users to create recipes and post
    them for others to view.

-   A simple but useful search system needs to be included.

-   The search function should allow the user to search by ingredients,
    ethnicity, time of day, and type.

*User Stories/Informal Sepcs*
-----------------------------

-   How do you see the Search Function Working?

-   How do you see the Display of recipes working?

-   How do you see the user profile page working?

*Type of Software*
------------------

-   Web Service

-   Implemented as a website

    -   Framework: Django

    -   Programming Language: Python

    -   Web Host: Digital Ocean

    -   Database Backend: MySql

    -   CSS: Bootstrap

-   Will be made to be mobile friendly

-   Will be portable, since it can be run on any consumer device that
    can run a basic web browser.

*Base Features*
---------------

-   Repository/database that will contain recipes

    -   This repository will be search-able.

        -   Style

        -   Ethnicity

        -   Type

        -   Time of Day

        -   Ingredients

        -   ***Other?***

-   User Profile Infrastructure

    -   Login/Logout/Registry System

    -   User Name

    -   User Avatar

    -   User created recipes

    -   User should be able to rate other user's recipes

-   Community Infrastructure

    -   Staff Picks

        -   Favorite Cooks/Users

        -   Favorite recipes

    -   Top Rated Recipes of the week

    -   etc...

-   Recipe Display

    -   Recipe Image uploaded by user who created/uploaded the recipe

    -   Necessary ingredients and the amount needed

    -   Estimated Time of Completion

    -   Steps to complete

        -   **Format of the step may be left up to the user?**

        -   **Textbox?**

        -   **Preformatted List?**

    -   Tags associating this recipe with specific search terms

        -   Ex.

        -   Tags: Broccoli, Carrots, Breakfast, Eggs, Mexican

        -   These can be used for the query of recipes.

        -   Allow these tags to be displayed to the viewer of the
            recipes?

        -   Allow or force User to input tags?

-   \[Query\] "Search/Query of Recipes"

    -   Should be fast and simple

    -   Search by...

        -   Ingredients

            -   Ex.

            -   Carrots, Broccoli, Milk, Flour, etc...

        -   Ethnicity

            -   Ex.

            -   Mexican, Southern, Japanese, Swedish, etc...

        -   Time of day

            -   Ex.

            -   Morning/Breakfast, Lunch/Afternoon, Brunch, Linner,
                Brinner, Dreakfast, Dinner, etc...

        -   Recipe Name -Ex.

            -   Tacos, Ramen Soup, Burgers, Clam Chowder, etc...

            -   **Allow different recipes to have the same name?**

        -   **Tags?**

            -   Give each recipe a set to tags that will define what
                words will be linked to this recipe as a search term.

*Functional Requirements*
-------------------------

-   User Profile Creation

    -   Allow user to create a profile

        -   User Name

        -   Password

        -   **Full Name?**

        -   email address

        -   Food preferences

        -   Biography/User Description

        -   Keep a list of their favored recipes

-   Allow for querying of recipes.

-   **Allow viewing of other user's profile?**

    -   View their List of created Recipes

    -   View their favored Recipes

    -   View their name, email, bio, etc...

*Non-functional Requirements*
-----------------------------

-   Performance Time

    -   Needs to be fast

-   The site should look nice

    -   **Specific Style?**

    -   **Simple Style?**

    -   **Not Cluttered**

-   Secure

    -   **Allow users to hide personal information?**

-   Easy to add Recipes

    -   **Allow user a lot of freedom in the formatting?**

    -   **Restrict user to a specific format that is predefined?**
