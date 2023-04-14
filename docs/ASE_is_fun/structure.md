[//]: # (DDD in Django)

[//]: # (A project for the course "Advanced Software Engineering" at the DHBW Karlsruhe)

[//]: # (by Marc Gökce, 2023)

---

# Domain Driven Design in Django

###### Sperrvermerk

This project is a restructuring of my existing blog site (www.mkrabs.de) using Domain Driven Design principles, as
part of the Advanced Software Engineering course in the 6th semester at the Duale Hochschule of Karlsruhe. The project
code is publicly available on GitHub, but please note that I do not take any responsibility for the use of this
code / architecture or other mishaps you might write in other projects. I cannot be held liable for any negative
outcomes or poor grades resulting from the use of this code, as it is intended for educational purposes only.

_Use at your own risk, lmao._

###### Table of Contents

- [Introduction](#introduction)
    - [Overview of the project](#overview-of-the-project)
    - [Description of the requirements](#description-of-the-requirements)
    - [Explanation of the approach](#explanation-of-the-approach)
- [Analysis of Ubiquitous Language](#analysis-of-ubiquitous-language)
- [Domain Model](#domain-model)
    - [Definition of the entities, value objects, and aggregates](#definition-of-the-entities-value-objects-and-aggregates)
    - [Specification of the domain services](#specification-of-the-domain-services)
    - [Implementation of the repositories](#implementation-of-the-repositories)
- [Tactical Design Patterns](#tactical-design-patterns)
    - [Implementation of Domain Events](#implementation-of-domain-events)
    - [Use of Factory and/or Builder patterns](#use-of-factory-andor-builder-patterns)
    - [Application of Specification pattern](#application-of-specification-pattern)
    - [Explanation of the approach and benefits](#explanation-of-the-approach-and-benefits)
- [Programming Principles](#programming-principles)
    - [SOLID principles](#solid-principles)
    - [GRASP principles, especially Coupling and Cohesion](#grasp-principles-especially-coupling-and-cohesion)
    - [DRY principle](#dry-principle)
    - [Explanation of the approach and benefits](#explanation-of-the-approach-and-benefits-1)
- [Implementation of Clean Architecture](#implementation-of-clean-architecture)
    - [Plan and justification of a layered architecture](#plan-and-justification-of-a-layered-architecture)
    - [Implementation of at least two layers](#implementation-of-at-least-two-layers)
    - [Explanation of the approach and benefits](#explanation-of-the-approach-and-benefits-2)
- [Refactoring](#refactoring)
    - [Identification of code smells](#identification-of-code-smells)
    - [Application of at least two refactorings](#application-of-at-least-two-refactorings)
    - [Explanation of the approach and benefits](#explanation-of-the-approach-and-benefits-3)
- [Implementation of at least one Design Pattern](#implementation-of-at-least-one-design-pattern)
    - [Justification of the pattern used](#justification-of-the-pattern-used)
    - [Creation of UML diagrams before and after the pattern implementation](#creation-of-uml-diagrams-before-and-after-the-pattern-implementation)
- [Persistence Layer](#persistence-layer)
    - [Implementation of the persistence layer](#implementation-of-the-persistence-layer)
    - [Explanation of the approach and benefits](#explanation-of-the-approach-and-benefits-4)
- [Unit Testing](#unit-testing)
    - [Unit tests](#unit-tests)
    - [Integration tests](#integration-tests)
    - [Smoke tests](#smoke-tests)
    - [Use of mocks in testing](#use-of-mocks-in-testing)
    - [Adherence to ATRIP rules](#adherence-to-atrip-rules)
    - [Explanation of the approach and benefits](#explanation-of-the-approach-and-benefits-5)
- [Conclusion](#conclusion)
    - [Summary of the work done](#summary-of-the-work-done)
    - [Review of the benefits of using DDD principles](#review-of-the-benefits-of-using-ddd-principles)
    - [Future work and improvements](#future-work-and-improvements)
- [References](#references)

---


# Introduction

###### Chapter 1

## Overview of the project

<div style="text-align:center">
  <img style="max-height: 200px" src="resources/banner.png" alt="banner"/>
</div>

This paper is about restructuring an existing Django-based blog platform using Domain-Driven Design (DDD) principles for
the Advanced Software Engineering course at the Duale Hochschule Baden-Württemberg Karlsruhe. The project aims to
implement a blog platform that allows users to create and share their personal blogs, interact with other blogs, and
express their feelings through comments and reactions.

The goal of this project is to improve the overall architecture and design of the platform by incorporating DDD
principles and best practices in software engineering. This paper serves as a documentation of the process and decisions
made during the restructuring of the project.

## Description of the requirements

The main requirement for this project is to implement DDD principles and patterns in the existing blog platform. This
includes analyzing the ubiquitous language of the domain, using tactical DDD patterns such as Value Objects, Entities,
Aggregates, Repositories, and Domain Services, and implementing a clear and meaningful domain model.

Additionally, the project must adhere to programming principles such as SOLID, GRASP, and DRY. At least one design
pattern must be implemented and justified using UML diagrams. The project must also follow the Clean Architecture
principles, with a planned and justified layer architecture, and at least two layers implemented.

To ensure code quality, at least 10 unit tests must be implemented following the ATRIP rules and using mocks where
necessary. Code smells must be identified and at least two refactorings must be applied and justified.

## Explanation of the approach

To incorporate common python DDD principles whilst following Django design principles, the first step is to
analyze the ubiquitous language of the domain and define the domain model using Value Objects, Entities, Aggregates,
Repositories, and Domain Services. This helps to ensure a clear and consistent understanding of the domain and its
concepts.

Next, the Clean Architecture principles will be followed to define a clear and meaningful layer architecture. This will
help to decouple the domain logic from the infrastructure and ensure that the application is easily testable,
maintainable, and scalable.

Programming principles such as SOLID, GRASP, and DRY will be followed to ensure code quality and maintainability. Design
patterns will be used where necessary to solve common design problems and improve the overall architecture of the
platform.

Finally, unit tests will be implemented to ensure that the code behaves as expected and to catch any potential
regressions. Code smells will be identified and refactored using appropriate techniques to ensure a clean and
maintainable codebase.

To demonstrate each refactoring step or change, we will use examples from the code base at commit hash
[#`5f0837`](https://github.com/MKrabs/Blog/tree/5f0837dd26a84c0e7e2687a66cbd54fd4254c209), which represents the code
as it existed before the start of this project.

###### Back to top [▲](#table-of-contents)

---

# Analysis of Ubiquitous Language

###### Chapter 2

- [x] Überlegen wie domaine aussieht
- [ ] was macht diese aus.
- [x] was sind die wichtigsten Begriffe
- [x] was sind die wichtigsten Konzepte

## Domain Terms

The Analysis of Ubiquitous Language is a crucial step in the development of any software system, as it helps to
establish a common language and understanding between the development team and the stakeholders. This chapter will focus
on defining the domain terms, identifying the domain concepts, and creating a glossary to ensure that everyone involved
in the project has a clear understanding of the terminology used.

The first step in analyzing the ubiquitous language is to define the domain terms used in the project. These terms
should be identified from the project requirements and any other relevant documentation. In the case of our blog site
project, some of the domain terms we might identify include:


##### Blog Post

The blog post is the main concept of the project. It refers to the content created by users on the website, including
written text, images, and other media. Users can create blog posts to share their personal thoughts, documented
projects, or any other topic they wish to express in words or images. Blog posts can be read by any visitor to the site,
and users can interact with blog posts by commenting, liking, and reporting.

##### User

Users are individuals who have registered for an account on the blog site. They can create blog posts, comment on other
users' blog posts, like blog posts, and interact with other users on the platform. Users can also create a user profile
that contains personal information, including their name, profile picture, and bio. The user profile allows other users
to learn more about the user and their interests.

##### User Profile (or Portfolio)

User profiles, also referred to as portfolios, are collections of personal information and preferences that allow other
users to learn more about a particular user. The user profile contains personal information, including the user's name,
profile picture, and bio. It also contains personal tags that show the user's interests or link to other websites.

##### Comment

Comments are a feature of the blog site that allows users to provide feedback on blog posts. Users can leave comments on
blog posts written by other users, or on their own blog posts. Comments can be used to ask questions, provide feedback,
or engage in discussions with other users. Comments can be liked by other users, indicating agreement or support.

##### Tag

Tags are keywords or phrases that users can use to categorize their blog posts. Tags allow users to easily search for
content related to a particular topic. Users can add tags to their blog posts, and the tags will be displayed on the
post, making it easy for other users to find related content.

##### Heart (Like)

The heart, also referred to as a like, is a feature of the blog site that allows users to express their approval or
appreciation for a particular blog post or comment. Users can click the heart icon to like a blog post or comment,
indicating agreement or support.

##### Report

The report is a feature of the blog site that allows users to report offensive or inappropriate content. Users can
report a blog post or comment if they believe it violates the website's terms of use. The report allows the website
administrators to review the content and take appropriate action to ensure the safety and integrity of the platform.

###### Back to top [▲](#table-of-contents)

---

# Domain Model

###### Chapter 3

## Definition of the entities, value objects, and aggregates

value object: immutable / statisch
zB kategorie

Django using active records.

Not anymore, we ditched django.

## Specification of the domain services

## Implementation of the repositories

###### Back to top [▲](#table-of-contents)

---

# Tactical Design Patterns

###### Chapter 4

## Implementation of Domain Events

## Use of Factory and/or Builder patterns

## Application of Specification pattern

## Explanation of the approach and benefits

###### Back to top [▲](#table-of-contents)

---

# Programming Principles

###### Chapter 5

## SOLID principles

## GRASP principles, especially Coupling and Cohesion

## DRY principle

## Explanation of the approach and benefits

###### Back to top [▲](#table-of-contents)

---

# Implementation of Clean Architecture

###### Chapter 6

## Plan and justification of a layered architecture

## Implementation of at least two layers

## Explanation of the approach and benefits

###### Back to top [▲](#table-of-contents)

---

# Refactoring

###### Chapter 7

## Identification of code smells

## Application of at least two refactorings

## Explanation of the approach and benefits

###### Back to top [▲](#table-of-contents)

---

# Implementation of at least one Design Pattern

###### Chapter 8

## Justification of the pattern used

## Creation of UML diagrams before and after the pattern implementation

###### Back to top [▲](#table-of-contents)

---

# Persistence Layer

###### Chapter 9

## Implementation of the persistence layer

### Repository pattern

### Active record pattern

## Explanation of the approach and benefits

###### Back to top [▲](#table-of-contents)

---

# Unit Testing

###### Chapter 10

## Unit tests

## Integration tests

## Smoke tests

## Use of mocks in testing

## Adherence to ATRIP rules

- Automatic
- Thorough (Vollständig)
- Repeatable
- Independent
- Professional

## Explanation of the approach and benefits

###### Back to top [▲](#table-of-contents)

---

# Conclusion

###### and or summary

## Summary of the work done

## Review of the benefits of using DDD principles

## Future work and improvements

###### Back to top [▲](#table-of-contents)

---

# References

###### Written references used in the project

* https://docs.djangoproject.com/en/4.2/misc/design-philosophies/#models
* https://www.cosmicpython.com/book/preface (very nice)
* https://wiki.c2.com/?CouplingAndCohesion
* https://iktakahiro.dev/python-ddd-onion-architecture
* https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215
* https://github.com/jdiazromeral/django-ddd
* https://openbase.com/python/Django-ddd
* https://michalgodkowicz.medium.com/another-way-to-persist-ddd-aggregates-in-django-d148f4cad298
* https://www.apress.com/gp/blog/all-blog-posts/domain-driven-design-with-django/16172586
* https://thedomaindrivendesign.io/why-use-domain-driven-design/

###### Video References

* https://www.youtube.com/watch?v=hv-LiKQgN90
* https://www.youtube.com/watch?v=Ru2T4fu3bGQ

###### Back to top [▲](#table-of-contents)

---

_Thank you for reading._

[@MKrabs](https://www.github.com/MKrabs) - [Website](https://www.mkrabs.de)

[//]: # (Styles)
<style>

ol { list-style-type: upper-roman; }
ol ol { list-style-type: decimal; }

</style>
