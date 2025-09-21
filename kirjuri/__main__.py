import click

from .processor import Processor
from .load import load


@click.command()
@click.argument('video_id')
@click.argument('output_file')
def main(video_id, output_file):
    """Fetch YouTube transcript and print length."""
    processor = Processor(load(video_id))
    with open(output_file, "w") as f:
        f.write(processor.dump())


if __name__ == "__main__":
    main()