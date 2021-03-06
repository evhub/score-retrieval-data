import os
import traceback

from pdf2image import convert_from_path

from score_retrieval.constants import (
    arguments,
    get_dataset_dir,
    IMG_EXT,
    DPI,
    NONE_DPI,
)
from score_retrieval.data import datasets


def get_img_path(save_dir, name, i, dpi=DPI):
    """Get the path that the given image should be saved to."""
    if dpi == NONE_DPI:
        dpi = None
    base_path = os.path.join(save_dir, name)
    if dpi is None:
        return "{}_{}{}".format(base_path, i, IMG_EXT)
    else:
        return "{}_{}_{}{}".format(base_path, dpi, i, IMG_EXT)


def save_pages(pdf_path, name, save_dir, force=False):
    """Save all page of given pdf as image."""
    try:
        pages = convert_from_path(pdf_path, DPI)
    except Exception:
        traceback.print_exc()
        print("Failed to save {} -> {}/{}.".format(pdf_path, save_dir, name))
    else:
        for i, page in enumerate(pages):
            page_path = get_img_path(save_dir, name, i)
            if force or not os.path.exists(page_path):
                print("Saving {}...".format(page_path))
                page.save(page_path, os.path.splitext(page_path)[-1].lstrip("."))
                print("Saved {}.".format(page_path))
            else:
                print("Skipping {}...".format(page_path))


def migrate_pdfs(dataset=None, force=False):
    """Migrate all pdfs to images."""
    data_dir = get_dataset_dir(dataset)
    print("Migrating {}...".format(data_dir))
    for dirpath, _, filenames in os.walk(data_dir):
        for pdf_file in filenames:
            name, ext = os.path.splitext(pdf_file)
            if ext == ".pdf":
                pdf_path = os.path.join(dirpath, pdf_file)
                save_pages(pdf_path, name, dirpath, force)


if __name__ == "__main__":
    parsed_args = arguments.parse_args()
    if parsed_args.multidataset:
        for dataset in datasets:
            migrate_pdfs(dataset)
    else:
        migrate_pdfs(parsed_args.dataset)
