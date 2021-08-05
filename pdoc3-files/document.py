#!/usr/bin/env python
# coding: utf-8

"""Script pour l'extraction de DocString des fichier pythons pour la documentation générale.
Nécessite pdoc3:

`conda install -c conda-forge pdoc3`
"""

from pathlib import Path
import os
import pdoc
import codecs
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Analyse structurelle de graphe.

Par défaut, si aucun argument n'est spécifié, un dossier `doc/` est créé avec un fichier HTML de documentation par fichier python.

- Pour écrire en reStructuredText:
    `$ python document.py -t rst`

- Pour changer le dossier de sortie:
    `$ python document.py -o mon_dossier`

- Pour changer le dossier racine:
    `$ python document.py -i mon_dossier`
""",
        formatter_class=argparse.RawTextHelpFormatter,
        )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="Root dir of project",
        default=".",
        metavar="PATH",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output dir",
        default="doc",
        metavar="PATH",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=['html', 'rst'],
        default="html",
        metavar="TYPE",
    )

    args = vars(parser.parse_args())

    __docformat__ = "numpy"

    py_files = []

    for path, directories, files in os.walk(str(args['input'].absolute())):
        p = [Path(path).joinpath(f) for f in files]
        py_files += [e.absolute() for e in p if e.exists() and e.suffix == ".py"]

    try:
        py_files.remove(Path(__file__).absolute())
    except:
        pass

    context = pdoc.Context()

    modules = [pdoc.Module(pdoc.import_module(str(f)), context=context) for f in py_files]

    pdoc.link_inheritance(context)

    def recursive_htmls(mod, parent=""):
        yield parent + mod.name, mod.html(), mod.text()
        for submod in mod.submodules():
            yield from recursive_htmls(submod, parent + ".")


    args['output'].mkdir(exist_ok=True, parents=True)


    for mod in modules:
        for module_name, html, text in recursive_htmls(mod):
            if args['type'] == 'html':
                with codecs.open(args['output'].joinpath(module_name + ".html"), "w", "utf-8") as f:
                    f.write(html)
            if args['type'] == 'rst':
                with codecs.open(args['output'].joinpath(module_name + ".rst"), "w", "utf-8") as f:
                    f.write(text)