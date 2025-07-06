.. Immunity documentation master file, created by
   sphinx-quickstart on Tue Jul  1 22:31:26 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Immunity documentation
===========================

Тест диаграммы

.. mermaid::

   sequenceDiagram
     participant User
     participant Agent
     participant Server
     User->>Agent: Запуск приложения
     Agent->>Server: Регистрация агента
     Server-->>Agent: Конфигурация

Тест ссылок

См. раздел :ref:`installation` 
или :doc:`user_guide`

Тест директив 

.. note:: Важное примечание
   123
123

.. warning:: Предупреждение!
   123

.. danger:: Критическое предупреждение
   123

.. code-block:: python
   :linenos:
   :emphasize-lines: 3,5
      release = "0.8.2"
      version = "0.8"

      extensions = [
         "sphinx.ext.autodoc",
         "sphinx.ext.napoleon",
         "sphinx.ext.viewcode",
         "sphinx.ext.intersphinx",
         "sphinx.ext.todo",
         "sphinxcontrib.httpdomain",
         "sphinx_rtd_theme",
         "myst_parser",
      ]


.. toctree::
   :maxdepth: 2
   :caption: Contents:

