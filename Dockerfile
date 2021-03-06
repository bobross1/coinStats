FROM continuumio/miniconda3
COPY . /app
WORKDIR /app
RUN conda create -n env python
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN conda config --env --add channels conda-forge
# RUN conda install --file requirements.txt
RUN pip3 install streamlit beautifulsoup4 pandas requests
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["dashboard.py"]