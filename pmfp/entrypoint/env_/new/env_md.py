import pkgutil
import warnings
import shutil
from pathlib import Path
from pmfp.utils.template_utils import template_2_content


sidebar_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', '_sidebar.md.jinja')
if template_io:
    sidebar_template = template_io.decode('utf-8')
else:
    raise AttributeError("_sidebar.md.jinja模板失败")

index_html_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'index.html.jinja')
if template_io:
    index_html_template = template_io.decode('utf-8')
else:
    raise AttributeError("index.html.jinja模板失败")


sidebar_css = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'sidebar.css.jinja')
if template_io:
    sidebar_css = template_io.decode('utf-8')
else:
    raise AttributeError("sidebar.css.jinja模板失败")


sidebar_folder_css = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'sidebar-folder.css.jinja')
if template_io:
    sidebar_folder_css = template_io.decode('utf-8')
else:
    raise AttributeError("sidebar-folder.css.jinja模板失败")


def init_md_env(cwd: Path, project_name: str, description: str) -> None:
    docs_path = cwd.joinpath("docs")
    if docs_path.exists():
        warnings.warn("docs已存在!")
        return
    else:
        docs_path.mkdir(parents=True)
        index_html_path = docs_path.joinpath("index.html")
        if not index_html_path.exists():
            content = template_2_content(
                template=index_html_template,
                project_name=project_name,
                description=description)
            with open(index_html_path, "w", newline="", encoding="utf-8") as f:
                f.write(content)
        _sidebar_md_path = docs_path.joinpath("_sidebar.md")
        if not _sidebar_md_path.exists():
            content = sidebar_template
            with open(_sidebar_md_path, "w", newline="", encoding="utf-8") as f:
                f.write(content)
        nojekyll_path = docs_path.joinpath(".nojekyll")
        if not nojekyll_path.exists():
            nojekyll_path.touch()
        nojekyll_path = docs_path.joinpath(".nojekyll")
        if not nojekyll_path.exists():
            nojekyll_path.touch()
        readme_path = docs_path.joinpath("README.md")
        if not readme_path.exists():
            cwd.joinpath("README.md")
            shutil.copyfile(cwd.joinpath("README.md"), readme_path)
        # css
        css_path = docs_path.joinpath("css")
        if not css_path.exists():
            css_path.mkdir(parents=True)

        sidebar_css_path = css_path.joinpath("sidebar.css")
        if not sidebar_css_path.exists():
            content = sidebar_css
            with open(sidebar_css_path, "w", newline="", encoding="utf-8") as f:
                f.write(content)
        sidebar_folder_css_path = css_path.joinpath("sidebar-folder.css")
        if not sidebar_folder_css_path.exists():
            content = sidebar_folder_css
            with open(sidebar_folder_css_path, "w", newline="", encoding="utf-8") as f:
                f.write(content)
