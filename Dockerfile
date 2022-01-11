# FROM python:3.10.1
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# EXPOSE 8501
# ENTRYPOINT ["streamlit", "run"]
# CMD ["dashboard.py"]

FROM continuumio/miniconda3
COPY . /app
WORKDIR /app
# RUN conda config --append channels conda-forge 
RUN conda create -n env python
# RUN conda config --append channels conda-forge
# RUN conda install --file requirements.txt
# RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN conda config --env --add channels conda-forge
RUN conda install --file requirements.txt
RUN pip install streamlit
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["dashboard.py"]