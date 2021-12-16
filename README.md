# Video Journal

## Table of contents

1. [Description](#desc)
2. [Installation](#install)

<a name="desc"/>

## Description

![Structure](https://github.com/aza-atabayev/video_journal/blob/main/structure.png?raw=true)

This is a repository of video journaling web app. After recording audio and video from webcamera, webapp saves the video and partitions it based on the emotions experienced by the user.

Emotion detection consists of 2 modules - video and audio. Video module uses Face Detection and runs Facial Expression Recognition model on the detected face. For Face detection OpenCV implementation of Haar Cascade Classifier was used with pre-trained weights provided by OpenCV. Facial Expression Recognition uses DAN (Distract your Attention Network) implementation of [yoing](https://github.com/yaoing/DAN) with provided pre-trained weights. 

Audio module converts speech to text, then runs punctuation restoration to identify start and the end of the sentence. Then, text Sentiment Analysis is run on each sentence. Speech to text conversion implementation of LSTMP (Long Short-Term Memory Projection) is used in [VOSK API](https://github.com/alphacep/vosk-api), a toolkit for Audio and Speech Research, with a pre-trained model. [Punctuation restoration](https://github.com/NVIDIA/NeMo) uses a pre-trained model BERT with two-token classification heads for punctuation and capitalization. [Text sentiment analysis](https://github.com/flairNLP/flair) is based on a character-level LSTM. 


<a name="install"/>

## Installation
For the installation you need to pre-install Conda.

```
git clone https://github.com/aza-atabayev/video_journal.git
cd video_journal
conda env create -n <env_name> -f environment.yml
conda activate <env_name>
```
After the installation download the following weights and put them in the respective directories:
- [MSCeleb](https://drive.google.com/file/d/1H421M8mosIVt8KsEWQ1UuYMkQS8X1prf/view) in /DAN/models
- [Affectnet8](https://drive.google.com/file/d/1uHNADViICyJEjJljv747nfvrGu12kjtu/view) in /DAN/checkpoints 
- [VOSK Speech-to-Text](https://drive.google.com/file/d/1-GCK1n7aV2wC1_dRoMT_3F47bEkapJMq/view?usp=sharing)
 in ./
 
 
In order to start the webapp run start_server.sh. The webapp will be available at localhost:5000.

```
bash start_server.sh
```
