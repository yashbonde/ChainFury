FROM node:16-alpine3.14 as builder
WORKDIR /app
COPY ./client/package*.json ./client/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY ./client .
RUN yarn build
ENV NODE_ENV production

FROM python:3.9
RUN mkdir /app
COPY ./requirements.txt /app
# Setting up the working directory
WORKDIR /app
RUN python3 -m pip install -r requirements.txt

# Bundle app source
COPY ./server /app
COPY --from=builder /app/dist ./static
RUN ls -la
COPY --from=builder /app/dist/index.html ./templates/index.html

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
