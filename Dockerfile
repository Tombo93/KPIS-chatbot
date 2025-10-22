FROM conda/miniconda3

WORKDIR /app

COPY environment.yml /app/environment.yml

RUN conda env create -f /app/environment.yml

RUN echo "source activate kpis-chatbot" > ~/.bashrc

ENV PATH /opt/conda/envs/kpis-chatbot/bin:$PATH

EXPOSE 8888

CMD [ "conda". "run", "-n", "kpis-chatbot" ]