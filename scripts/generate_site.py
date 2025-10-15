import os
import re

def generate_site():
    """
    Generates a static recipe site from text files.
    """
    # Create the output directory
    if not os.path.exists("_site"):
        os.makedirs("_site")

    # Get all recipe files
    recipe_files = [f for f in os.listdir("recipes") if os.path.isfile(os.path.join("recipes", f))]

    # Generate the index page
    with open("_site/index.html", "w", encoding='utf-8') as index_file:
        index_file.write("<!DOCTYPE html>\n")
        index_file.write("<html lang=\"en\">\n")
        index_file.write("<head>\n")
        index_file.write("    <meta charset=\"UTF-8\">\n")
        index_file.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        index_file.write("    <title>My Recipe Blog</title>\n")
        index_file.write("    <style>\n")
        index_file.write("        body { font-family: sans-serif; line-height: 1.6; padding: 2em; }\n")
        index_file.write("        ul { list-style-type: none; padding: 0; }\n")
        index_file.write("        li { margin-bottom: 1em; }\n")
        index_file.write("        a { text-decoration: none; color: #0066cc; }\n")
        index_file.write("    </style>\n")
        index_file.write("</head>\n")
        index_file.write("<body>\n")
        index_file.write("    <h1>My Recipes</h1>\n")
        index_file.write("    <ul>\n")

        recipes_with_titles = []
        for recipe_file in recipe_files:
            with open(os.path.join("recipes", recipe_file), "r", encoding='utf-8', errors='ignore') as f:
                first_line = f.readline().strip()
                # Use filename as title if first line is long or empty
                if len(first_line) > 50 or not first_line:
                    title = os.path.splitext(recipe_file)[0]
                else:
                    title = first_line
                recipes_with_titles.append({'filename': recipe_file, 'title': title})

        # Sort by title
        recipes_with_titles.sort(key=lambda x: x['title'])

        for recipe in recipes_with_titles:
            # Generate a safe filename for the link
            safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', recipe['filename']) + ".html"
            index_file.write(f"        <li><a href=\"{safe_filename}\">{recipe['title']}</a></li>\n")

        index_file.write("    </ul>\n")
        index_file.write("</body>\n")
        index_file.write("</html>\n")

    # Generate individual recipe pages
    for recipe_file in recipe_files:
        with open(os.path.join("recipes", recipe_file), "r", encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            first_line = lines[0].strip()
            # Use filename as title if first line is long or empty
            if len(first_line) > 50 or not first_line:
                title = os.path.splitext(recipe_file)[0]
                content = "".join(lines)
            else:
                title = first_line
                content = "".join(lines[1:])

            safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', recipe_file) + ".html"
            with open(os.path.join("_site", safe_filename), "w", encoding='utf-8') as recipe_page:
                recipe_page.write("<!DOCTYPE html>\n")
                recipe_page.write("<html lang=\"en\">\n")
                recipe_page.write("<head>\n")
                recipe_page.write("    <meta charset=\"UTF-8\">\n")
                recipe_page.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
                recipe_page.write(f"    <title>{title}</title>\n")
                recipe_page.write("    <style>\n")
                recipe_page.write("        body { font-family: sans-serif; line-height: 1.6; padding: 2em; }\n")
                recipe_page.write("        pre { white-space: pre-wrap; font-family: inherit; }\n")
                recipe_page.write("    </style>\n")
                recipe_page.write("</head>\n")
                recipe_page.write("<body>\n")
                recipe_page.write(f"    <h1>{title}</h1>\n")
                recipe_page.write(f"    <pre>{content.strip()}</pre>\n")
                recipe_page.write("    <a href=\"index.html\">Back to all recipes</a>\n")
                recipe_page.write("</body>\n")
                recipe_page.write("</html>\n")

if __name__ == "__main__":
    generate_site()
    print("Site generated successfully in _site directory.")