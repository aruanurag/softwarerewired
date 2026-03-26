---
title: "The True Cost of Serverless: What Architects Should Know"
date: 2026-03-15
author: "Software Rewired"
tags: ["Software Architecture", "SaaS", "AI Platforms"]
summary: "Serverless is freeing, but it's not free. A practical look at billing models and the architecture decisions that drive costs."
---

Serverless is freeing, but it's not free.

We love that serverless lets us run code without managing infrastructure. But behind the scenes, every millisecond and megabyte is metered. When you hit scale or use the wrong pattern, those tiny costs add up.

This post breaks down how serverless billing works across AWS, Azure, GCP, and OCI—and why understanding your architecture patterns is just as important as understanding pricing.

---

### How Serverless Billing Works

Every cloud provider follows a similar model:

- **You choose memory size** when defining a function
- **They measure how long it runs** (execution time)
- **They charge you for the number of invocations**

Some include a generous free tier. Some bundle CPU and memory. Some add minimum charges per execution. But the core principle is the same: 

> **You pay for memory size × execution time × number of invocations**

---

### Real-World Example: The Fan-Out Pattern

A customer once used a fan-out model where one input triggered dozens of downstream functions. Each message was fanned out across queues, with functions processing them in parallel. Great for decoupling, but they didn’t set limits or budgets.

Each of those parallel executions added cost. And the functions weren’t optimized either: default templates, overprovisioned memory, no batching. Their cloud bill shot up before anyone realized what was happening.

---

### Key Cost Drivers

Here are a few things that impact serverless pricing the most:

#### 1. **Memory Size**
More memory means faster execution (more CPU), but a higher rate. Sometimes doubling memory can halve execution time, which lowers cost—but not always. You need to test.

#### 2. **Execution Time**
Every millisecond counts. GCP bills in 100ms chunks. Azure rounds up to 100ms. AWS and OCI use millisecond granularity. A slow-running function gets expensive fast.

#### 3. **Invocation Count**
You’re charged for every call. Fan-out, retries, and event noise can multiply costs.

#### 4. **Free Tiers**
Free usage varies. AWS, Azure, and OCI offer 1–2 million free invocations and 400,000 GB-seconds monthly. GCP offers 2 million calls and free CPU + memory usage.

---

### Comparing Billing Models

Let’s say you run 1 million invocations of a 128MB function for 100ms each. That’s 12,800 GB-seconds of compute.

- **AWS & Azure:** 1M calls and 400K GB-s are free. You only pay for the extra 12.4K GB-s.
- **GCP:** Even more generous. 2M free invocations, 400K GB-s, and 200K GHz-s. You likely won’t pay anything unless you scale more.
- **OCI:** Similar model to AWS, with 2M free calls and 400K GB-s monthly.

---

### Beyond Pricing: It’s About Architecture

Cost is just one piece. Serverless has amazing agility and scale, but it’s not the answer to every problem. Some things to consider:

- **Are your functions short-lived? ** Long-running tasks might be cheaper in containers or VMs.
- **Can you batch or debounce?** Fewer calls = lower cost.
- **Do you need high concurrency?** Cold starts and platform limits can hit performance.
- **Do you control downstream costs?** Serverless might be cheap, but logging, messaging, and storage often aren't.

---

### Why This Matters

Serverless is a powerful tool. But we should treat it like any architecture decision—evaluate, test, optimize.

Start with the problem you’re solving, not the trend you’re chasing.

Sometimes the most cost-effective solution is a better architecture.

---

### References:
1. [AWS Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
2. [Azure Functions Pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)
3. [Google Cloud Functions Pricing](https://cloud.google.com/functions/pricing)
4. [Oracle Cloud Functions Pricing](https://www.oracle.com/cloud/functions/pricing/)
5. [AWS Serverless Patterns and Cost Optimization](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
6. [Google Cloud Serverless Best Practices](https://cloud.google.com/architecture/serverless-best-practices)
7. [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
8. [Serverless Cost Optimization Guide (GCP)](https://cloud.google.com/blog/products/serverless/optimizing-costs-for-cloud-functions)
