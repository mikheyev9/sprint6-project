![GitHub Workflow Status](https://img.shields.io/badge/Graphviz-required-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![PlantUML](https://img.shields.io/badge/PlantUML-1.2023.13-orange)

Этот проект использует Diagrams, PlantUML и Graphviz для генерации и визуализации диаграмм.

---

## 📊 Работа с диаграммами

### Установка Diagrams.
1. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

2. **Установка Graphviz**
   - Скачайте установщик для вашей ОС: [Graphviz Download](https://graphviz.org/download/)
   - При установке выберите опцию **"Add Graphviz to PATH"**

3. **Генерация диаграмм**
   ```bash
   python -m diagram_user
   ```

---

### Установка PlantUML.
1. Откройте файлы `*.puml` в вашем редакторе
2. Используйте синтаксис PlantUML для модификации
3. Рекомендуемые инструменты:
   - [VS Code с расширением PlantUML](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)
   - [IntelliJ/PyCharm Plugin](https://plugins.jetbrains.com/plugin/7017-plantuml-integration)
4. Убедитесь, что у Вас установлен Graphviz(см.выше).
5. В файле plantuml_user правой кнопкой мыши и выбере "Preview Cureent Diagram"
6. Или используйте [PlantUML Web Server](https://www.plantuml.com/plantuml/uml/):
   - Скопируйте содержимое `*.puml` файла
   - Вставьте в поле на сайте
   - Скачайте результат в форматах PNG/SVG

---
