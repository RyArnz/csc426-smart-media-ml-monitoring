\---

marp: true
size: 4:3
paginate: true
title: Final Project Rubric
---

# Final Project Rubric

* This is a **self-evaluation** rubric. Evaluate yourself as a professional problem solver.
* **Note:** This rubric covers the 500-point self-evaluation portion (project + learning with AI) and the 100-point evaluation of peers. HW (150 points) and midterm (250 points) are graded separately.
* All-or-nothing grading for each item (No partial points)
* Make sure to change the rubric file name correctly before submission
* Make sure you fill in all the (?) or ? marks with correct information

  * Use (V) for OK and (X) for not OK

\---

## Information

- Name: Ryan Arnzen
- Email: arnzenr1@nku.edu

---

## Summary

- One-line description of your project (focus on the problem you solved): 
I built a self-hosted smart home media server that combines remote media streaming, public cloud storage, live monitoring, and Raspberry Pi-based physical telemetry into one system.

- Why solving this problem is important: 
This problem is important because home users often depend on separate third-party services for media, storage, and visibility into system health. By solving it with a self-hosted platform, I got to learn practical skills in Linux, Docker deployment, networking, reverse proxy access, monitoring, and hardware integration while creating a system I can use. 

- Your approach/solution: 
My solution was to build the system on Ubuntu Server using Dockerized services. Plex provides local and remote media access, Nextcloud provides domain-accessible cloud storage, and Prometheus, Grafana, node_exporter, and cAdvisor provide live host and container monitoring. I also extended the system with a Raspberry Pi status panel that reflects server health through physical LED indicators.

- Technology stack used: 
Ubuntu Server, Docker, Docker Compose, Plex, Nextcloud, Nginx Proxy Manager, Prometheus, Grafana, node_exporter, cAdvisor, Raspberry Pi 4, Python 3, and gpiozero.

- Your two Learning with AI topics:
  - Topic 1: Linux, Docker, and self-hosted deployment
  - Topic 2: Monitoring, observability, and Raspberry Pi telemetry integration

- Link to your Canvas page: https://nku.instructure.com/courses/88152/pages/individual-progress-ryan-arnzen
- Link to your GitHub repository: https://github.com/RyArnz/csc494-smart-media-server

For Grading 1 & 2, you self-evaluate your problem definitions & solutions uploaded to GitHub & Canvas pages.

\---

## Grading 1 - Project (300 points total)

Use the answers for your Marp slides.

### 1.1 Solving Problems (50 points)

#### Problem Domain (25 points)

* Use the answer for your resume
* Use this question/answer format for your future problem-solving
* (V) I clearly defined the problem I am solving.
* (V) I explained why this problem is important to solve.
* (V) My problem definition is accessible to my managers via Canvas or GitHub.

Describe your problem domain in your own words:
The problem I am trying to solve is having several subscriptions and never owning any of your own data or media. By spending money every month back to back you are stuck in an endless cycle and become more reliant on the service you are using.



**Grading Scale:**

* 90-100%: I am confident that I clearly defined a meaningful problem and convincingly explained its importance; my managers can easily find and understand it.
* 70-89%: I defined the problem and explained its importance, but some parts could be clearer or more accessible to my managers.
* 50-69%: I attempted to define the problem, but the definition is vague or the importance is not well explained.
* 30-49%: My problem definition is incomplete or unclear, and my managers would struggle to understand it.
* 0-29%: I did not define the problem, or the definition is missing entirely.

**Points in Percentage**: (100)/100%
**Points:** (25)/25

\---

#### Solution Domain (25 points)

* Also, use the answer for your resume
* Use this question/answer format for your future problem-solving
* (V) I clearly described my proposed solution.
* (V) I explained how my solution addresses the problem.
* (V) My solution design is documented and accessible to my managers.

Describe your solution domain in your own words:
My solution is to create an at home server to handle cloud storage needs across devices. It also handles my streaming needs eliminating the need for subscriptions to multiple platforms.



**Grading Scale:**

* 90-100%: I am confident that I proposed a well-designed solution that clearly addresses the problem; it is fully documented and accessible.
* 70-89%: I described a reasonable solution and how it addresses the problem, but documentation or accessibility could be improved.
* 50-69%: I described a solution, but the connection to the problem is weak, or the documentation is incomplete.
* 30-49%: My solution description is vague, and it is unclear how it solves the problem.
* 0-29%: I did not describe a solution, or the description is missing entirely.

**Points in Percentage**: (100)/100%
**Points:** (25)/25

\---

### 1.2 Implementation (150 points)

#### Technology (Tools) Stack (50 points)

* (V) I clearly described the technology stack (tools) I used.
* (V) I explained why I chose this technology stack for this problem.
* How you solved the problems with the technology stack (tools) with AI:

I used AI to discover different technologies and find out where different technology outperforms others. AI was very helpful in determining which application to implement and how they all communicate together.



* The technology stack I used:

Ubuntu Server

Docker / Docker Compose

Plex

Nextcloud

Nginx Proxy Manager

Prometheus

Grafana

node\_exporter

cAdvisor

Raspberry Pi 4

Python 3

gpiozero





**Grading Scale:**

* 90-100%: I am confident that I clearly described the technology stack and provided a strong justification for why it was the right choice for my problem.
* 70-89%: I described the technology stack and gave a reasonable justification, but the reasoning could be more specific or thorough.
* 50-69%: I listed the technology stack, but the justification for choosing it is weak or missing.
* 30-49%: My technology stack description is incomplete or the choice seems unrelated to the problem.
* 0-29%: I did not describe the technology stack or it is missing entirely.

**Points in Percentage**: (100%)/100%
**Points:** (50)/50

\---

#### Demonstration Video (50 points)

* (V) I created a demonstration video clip showing my project results.
* (V) The video is accessible to my managers and the class.
* The link to my demonstration video:

https://youtube.com/shorts/-h2SgqsmxSU?feature=share

https://github.com/RyArnz/csc494-smart-media-server/blob/main/ServerDemo.mp4



**Grading Scale:**

* 90-100%: I am confident that my demonstration video clearly shows working project results and is easily accessible to anyone.
* 70-89%: I created a demonstration video showing results, but it could be clearer or more complete in what it demonstrates.
* 50-69%: I created a video, but it is difficult to follow, incomplete, or hard to access.
* 30-49%: My video is very rough, does not clearly demonstrate results, or has accessibility issues.
* 0-29%: I did not create a demonstration video or the link is missing/broken.

**Points in Percentage**: (100%)/100%
**Points:** (50)/50

\---

#### Marp Presentation (50 points)

* (V) I created a high-quality Marp presentation PDF with video clips for my final presentation.
* (V) The presentation PDF is uploaded to GitHub and accessible to anyone.
* The link to my Marp presentation PDF:

https://github.com/RyArnz/csc494-smart-media-server/blob/main/Slides/FinalPresentation.pdf



**Grading Scale:**

* 90-100%: I am confident that my Marp presentation is professional, clearly communicates my project with video clips, and is publicly accessible on GitHub.
* 70-89%: I created a Marp presentation that covers the key points, but it could be more polished, better organized, or video clips are missing.
* 50-69%: I created a presentation, but it is missing important content or does not fully represent my project results.
* 30-49%: My presentation is incomplete, hard to follow, or not properly uploaded and accessible.
* 0-29%: I did not create a Marp presentation or the link is missing/broken.

**Points in Percentage**: (100%)/100%
**Points:** (50)/50

\---

### 1.3 Progress According to the Plan (100 points)

#### Weekly Updates (100 points)

* (X) I have regularly updated my individual progress on Canvas.
* (V) I have regularly updated my project artifacts (code, documents) on GitHub.
* (V) My weekly updates are clearly accessible by my managers.

Provide a brief summary of your weekly progress:

* Week 1: 1:

\- Ubuntu Server flashed onto laptop. 

\- Docker Installed, Disk partitioned for OS, Media, and nextcloud.



* Week 2:

\- Laptop Issues and Linux server reinstall.



* Week 3:

Installed Nextcloud, Plex, and Nginx Proxy Manager.

\- Used AI to learn about reverse proxy, proxy, exposing ports, CloudFlare tunneling.  



Week 4:

\- Created arnzenserver.org domain through namecheap.

\- Connected to a CloudFlare for DNS management.

\- Configured cloudflare tunnel connections to communicate with server without opening router ports. 

\- Setup Docker Bridge network to allow containers to communicate without exposing applications directly to LAN.

\- Deployed Nginx to handle incoming requests and proxy them to container ports (plex:32400, nextcloud: 80).



Week 6:

\- As of week 6 cloud.arnzenserver.org subdomain worked and allowed file upload and download.

\- Media.arnzenserver.org only worked locally, when accessed via domain opened up the Nginx welcome screen. 



Week 7:

\- Created presentation.

\- Updated Git Repo.

\- I believe the problem was trying to use two tunnel connection into my network, but will test to make sure in sprint two. 



Week 8:

\- Reworked external service routing.

\- Verified Cloudflare Tunnel and Nginx Proxy Manager behavior.

\- Confirmed public domain-based routing path for both major services:

cloud.arnzenserver.org

media.arnzenserver.org

Final architecture now routes:

\- cloud.arnzenserver.org → Cloudflare Tunnel → Nginx Proxy Manager → Nextcloud

\- media.arnzenserver.org → Cloudflare Tunnel → Nginx Proxy Manager → Plex



Week 9:

\- Successfully got Plex working externally through media.arnzenserver.org.

\- Verified Plex local access and domain-based external access.

\- Verified Nextcloud external access through cloud.arnzenserver.org.

\- Confirmed Cloudflare Tunnel routing and Nginx Proxy Manager routing were both working.



Week 10:

\- Added monitoring stack components:

Prometheus

Grafana

node\_exporter

cAdvisor

\- Verified that Prometheus was collecting metrics.

\- Verified dashboards were working in Grafana.

\- Verified host and container monitoring. The presentation lists CPU, RAM, disk, uptime, container memory, container CPU, and container count as monitored values.



Week 11/12:

\- Worked on python AI model.



Week 13/14:

\- Integrated Raspberry Pi 4 into the project for physical server-health output.

\- Designed a Python-based LED status system.

\- Wired LED indicators and verified hardware operation.

\- Final LED design:

Green = server reachable

Blue = Plex healthy

Yellow = warning

Red = critical issue / disk or service problem



\- Improved Project Documentation

&#x20;

**Grading Scale:**

* 90-100%: I am confident that I updated my progress and artifacts consistently every week; my managers could always track my work without asking.
* 70-89%: I updated my progress most weeks, but there were a few gaps or updates were not always detailed enough.
* 50-69%: I updated my progress, but updates were irregular, incomplete, or hard for managers to find.
* 30-49%: My updates were very infrequent and managers would have had difficulty tracking my progress.
* 0-29%: I did not provide regular updates or there are no visible updates on Canvas or GitHub.

**Points in Percentage**: (75%)/100%
**Points:** (75)/100

\---

## Grading 2 - Learning with AI (200 points)

### Topic 1 (100 points)

* Topic name: Linux, Docker, Networking, Reverse Proxy, and Cloudflare Tunnel for Secure Remote Access
* (V) I clearly explained what I learned from AI about this topic.
* (V) I interpreted the topic in my own words (not just copy-pasting from AI).
* (V) I created a high-quality Marp PDF slide for this topic.
* (V) The slide is publicly accessible (anyone can download it).
* The link to my Topic 1 Marp PDF slide: https://github.com/RyArnz/csc494-iot-ai-learning/blob/main/Slides/Topic%201.md



What I learned and my interpretation:

I learned how to set up an Ubuntu server and deploy containerized services with Docker. I also learned networking concepts such as port forwarding, reverse proxying, and tunneling. I learned secure remote access is built from multiple layers instead of one simple setting. AI helped me understand how Cloudflare Tunnel, Nginx Proxy Manager, DNS, and Docker networking each play a different role in getting outside traffic safely to the correct service.



**Grading Scale:**

* 90-100%: I am confident that I deeply understood the topic, expressed it in my own words, and created a clear, publicly accessible Marp slide that others can learn from.
* 70-89%: I explained the topic and created a slide, but the interpretation could be more original or the slide could be more polished and accessible.
* 50-69%: I covered the topic, but my explanation heavily relies on AI-generated text rather than my own interpretation.
* 30-49%: My explanation is superficial or mostly copied from AI with little evidence of personal understanding.
* 0-29%: I did not submit a slide or the explanation is missing entirely.

**Points:** (100)/100

\---

### Topic 2 (100 points)

* Topic name: Monitoring with Prometheus, Grafana, and Raspberry Pi Health Indicators

* (V) I clearly explained what I learned from AI about this topic.
* (V) I interpreted the topic in my own words (not just copy-pasting from AI).
* (V) I created a high-quality Marp PDF slide for this topic.
* (V) The slide is publicly accessible (anyone can download it).
* The link to my Topic 2 Marp PDF slide: https://github.com/RyArnz/csc494-iot-ai-learning/blob/main/Slides/Topic%202.md

What I learned and my interpretation:

I learned how to setup monitoring so it is more than just looking at graphs. Each tool has its own purpose in tracking system health. AI helped me understand how Prometheus collects metrics, how Grafana displays them, how exporters provide the data, and how to use Raspberry Pi LEDs to turn that information into a simple physical status display.




**Grading Scale:**

* 90-100%: I am confident that I deeply understood the topic, expressed it in my own words, and created a clear, publicly accessible Marp slide that others can learn from.
* 70-89%: I explained the topic and created a slide, but the interpretation could be more original or the slide could be more polished and accessible.
* 50-69%: I covered the topic, but my explanation heavily relies on AI-generated text rather than my own interpretation.
* 30-49%: My explanation is superficial or mostly copied from AI with little evidence of personal understanding.
* 0-29%: I did not submit a slide or the explanation is missing entirely.

**Points:** (100)/100

\---

## Grading 3 - Evaluating Peers (100 points)

### Self-Evaluation as a Manager

* I am managing these three peers:

  * Student 1: Devyn Ferman
  * Student 2: Jeffrey Perdue
  * Student 3: Josh Spencer
* (V) I have kept track of my three peers' progress regularly throughout the project.
* (V) I monitored both their project results and progress reports on Canvas.
* (V) I will submit my peer evaluation using the peer evaluation rubric.
* (V) I will submit my peer evaluation before the deadline.
* (V) I understand that failure to submit peer evaluations may result in failure of this course.
* (V) I will evaluate my peers professionally, fairly, and honestly.

**Grading Scale:**

* 90-100%: I am confident that I actively tracked all three peers throughout the project and will submit a thorough, fair, and professional evaluation.
* 70-89%: I tracked my peers' progress for most of the project, but my monitoring was not fully consistent.
* 50-69%: I checked on my peers occasionally but did not maintain regular tracking throughout the project.
* 30-49%: I did minimal peer monitoring and my evaluation will be based on limited observation.
* 0-29%: I did not track my peers or I do not plan to submit the peer evaluation.

**Points:** (100)/100

\---

## Total Self-Grading Summary

|Category|Points|Comment|
|-|-|-|
|1.1 Solving Problems|( (50) / 50)||
|1.2 Implementation|( (150) / 150)||
|1.3 Progress According to Plan|( (75) / 100)||
|2. Learning with AI|( (200) / 200)||
|**Total Points**|**( (475) / 500)**||

|Category|Points|Comment|
|-|-|-|
|3. Evaluating Peers|( (100) / 100)||
|**Total Points**|**( (100) / 100)**||

\---

## Checklist Before Submission

* (V) I checked that all rubric items are graded; no ? marks remain.
* (V) I filled in all the requested links (Canvas, GitHub, video, slides).
* (V) I understand the grading rules and have followed the rubric guidelines.
* (V) I uploaded this rubric file with the correct name: `Arnzen\\\\\\\_Ryan\\\\\\\_project\\\\\\\_rubric.md`
* (V) I will upload my peer evaluation using the peer evaluation rubric file.
* (V) I understand this assignment will be regraded and points can be deducted (up to 100%) if:

  * Any violation of academic integrity is detected
  * The rubric guidelines are not followed
  * The content is of low quality

