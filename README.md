[//]: # (DDD in Django)

[//]: # (A project for the course "Advanced Software Engineering" at the DHBW Karlsruhe)

[//]: # (by Marc Gökce, 2023)

# Domain Driven Design in Python 🐍

---

###### Sperrvermerk

This project is a _restructuring_ of my existing blog site (www.mkrabs.de) using Domain Driven Design
principles, as part of the Advanced Software Engineering course in the 6th semester at the Duale Hochschule of
Karlsruhe. The project code is publicly available on GitHub, but please note that I do not take any responsibility
for the use of this code / architecture or other mishaps you might write in other projects. I am not liable for any
negative outcomes, poor grades or broken snakes resulting from the use of this code, as it is intended for educational
purposes only.

_Use at your own risk, lmao._

---

###### Table of Contents

Will update as time marches on



---

This project uses python as the programming language and Django as the overlord framework. This is how I plan to 
structure the project: It will incorporate 3 main layers: domain, application and infrastructure, whilst using some 
lesser important ones like abstraction and presentation.

### Domain

The Domain layer encompasses the crucial business logic and entities of the application, including user accounts, blog
posts, comments, and likes. It defines the fundamental concepts and behaviors of the application, and is composed of
pure Python code that is technology-agnostic and easy to comprehend and maintain. The entities within this layer serve
as the fundamental building blocks of the application and embody the core business requirements. Additionally, the
repository interfaces defined within this layer facilitate data access and manipulation. By separating domain-specific
concerns from implementation details, the Domain layer promotes better reasoning and modification of the application.

```
todo: add code
```

### Application

The Application layer encompasses the use cases and business logic of the application, dictating how the core entities
are utilized and manipulated to accomplish specific objectives, such as generating a blog post or commenting on a post.
This layer relies on the Domain layer and interfaces with the Infrastructure layer to execute necessary operations. The
services within this layer encapsulate the business logic and furnish a more elevated API for the presentation layer to
engage with. By dividing the business logic from implementation details, the Application layer streamlines the process
of adjusting and advancing the application.

```
todo: add code
```
### Infrastructure

The Infrastructure layer serves as a bridge between the Domain layer and the persistence layer, which is typically a
database or a file system. This layer is responsible for implementing the necessary infrastructure to enable the
application to interact with external systems, such as web APIs, file systems, or databases. The repositories defined
within this layer provide a way to persist and retrieve data from the underlying storage system. The implementation of
these repositories may vary depending on the chosen technology, such as ORM frameworks or raw SQL queries. The
Infrastructure layer is crucial because it isolates the application's business logic from the underlying implementation
details of external systems, ensuring flexibility and maintainability.

```
todo: add code
```
### Presentation

The Presentation layer encompasses the user interface and presentation logic of the application, dictating how users
engage with the application and how data is presented to them. This layer relies on the Application layer to retrieve
and manipulate data. The resources defined in this layer, including HTML, CSS, and JavaScript, determine the visual
aesthetics and behavior of the application. The primary Python file serves as the application's entry point and manages
user requests. The Presentation layer is important because it provides the necessary user-facing components, rendering
the application accessible and usable to individuals.

```
todo: add code
```
### Test

The Testing layer is dedicated to testing the application. Testing is an integral aspect of software development, as it
confirms the functionality of the application and identifies any defects or issues before release. The test directory is
segregated into two subdirectories: unit and smoke.

The unit directory contains unit tests that test the functionality of individual components in isolation. These tests
verify that each component of the application performs as expected independently of its interaction with other
components. Unit tests are crucial in ensuring that the application's building blocks function as intended.

The smoke directory contains integration tests that validate the integration between different layers of the
application. These tests ensure that the application's components communicate with each other correctly and that the
different layers interact with one another as intended. Integration tests are essential in guaranteeing the overall
behavior of the application.

Both types of tests are significant in ensuring the quality and correctness of the application. By writing tests,
developers can detect errors and issues early in the development process, reducing the costs and time required to
address them. Furthermore, tests serve as documentation for the application's behavior, simplifying the understanding
and modification of the code for future developers.

```
todo: add example of unit test and smoke test
```
---

# Conclusion

###### and or summary

## Summary of the work done

## Review of the benefits of using DDD principles

## Future work and improvements

###### Back to top [▲](#table-of-contents)

---

# References

###### Write the references used in the project

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