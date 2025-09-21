import click

from .processor import Processor
from .load import load


@click.command()
@click.argument("video_id")
@click.argument("output_dir", default="out")
def main(video_id, output_dir):
    """Fetch YouTube transcript and print length."""
    processor = Processor(load(video_id))
    processor.split_by_speaker()
    processor.split_by_silence(10)
    processor.split_by_note()
    processor.dump(output_dir)


if __name__ == "__main__":
    main()