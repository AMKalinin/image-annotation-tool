FROM continuumio/miniconda3

RUN apt update

RUN apt install -y pkg-config libhdf5-mpi-dev libhdf5-dev

RUN MPICC="mpicc -shared" pip install --no-binary=mpi4py mpi4py

RUN conda install -c defaults --override-channels numpy

RUN HDF5_MPI="ON" CC=mpicc pip install --no-binary=h5py h5py

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod +x /app/run.py

EXPOSE 5000

# CMD ["python", "/app/run.py"]
CMD cd /app; gunicorn -b 0.0.0.0:5000 -w 4 run:app