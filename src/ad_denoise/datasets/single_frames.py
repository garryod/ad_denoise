from torch import Tensor, float32, from_numpy
from torch.utils.data import Dataset

from .utils import H5Datasets, get_dataset_edges, open_datasets, read_frame_datasets


class SingleFrames(Dataset):
    """A pytorch dataset which loads individual frames from hdf5 datasets."""

    def __init__(self, datasets: H5Datasets, frame_dims: int = 2) -> None:
        """Creates a pytorch dataset which reads frames hdf5 datasets.

        Args:
            datasets: An iterable of hdf5 file paths and the key of the dataset to be
                read.
            frame_dims: The trailing dimensionality of the frame. Defaults to 2.
        """
        super().__init__()
        self.frame_dims = frame_dims
        self.datasets = open_datasets(datasets)
        self.edges = get_dataset_edges(self.datasets, self.frame_dims)

    def __len__(self) -> int:
        return self.edges[-1]

    def __getitem__(self, idx: int) -> Tensor:
        return (
            from_numpy(
                read_frame_datasets(self.datasets, idx, self.frame_dims, self.edges)
            )
            .unsqueeze(0)
            .type(float32)
        )
