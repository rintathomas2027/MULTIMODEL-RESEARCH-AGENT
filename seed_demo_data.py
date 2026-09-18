"""
ScholarPulse AI Studio - Demo Data Seeding Script
================================================
Populates the database with realistic AI research papers, vector embeddings,
and academic metadata to enable full testing and live demonstration of all 14 modules.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_assistant.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from users.models import UserProfile
from assistant.models import Document, ChatHistory
from assistant.services.chunker import chunk_text
from assistant.services.vector_store import store_document_chunks

PAPERS = [
    {
        "title": "Attention Is All You Need: The Transformer Architecture",
        "filename": "attention_is_all_you_need.txt",
        "summary_short": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose the Transformer, based solely on attention mechanisms.",
        "content": """Title: Attention Is All You Need
Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
Published: 2017 (NeurIPS 2017)
Identifier: arXiv:1706.03762

Abstract:
The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The Transformer model architecture eschews recurrence and instead relies entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.

1. Introduction
Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation. The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution.

2. Model Architecture
Most competitive neural sequence transduction models have an encoder-decoder structure. The encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence of continuous representations z = (z1, ..., zn). Given z, the decoder then generates an output sequence (y1, ..., ym) of symbols one element at a time.

2.1 Scaled Dot-Product Attention
We call our particular attention "Scaled Dot-Product Attention". The input consists of queries and keys of dimension dk, and values of dimension dv. We compute the dot products of the query with all keys, divide each by sqrt(dk), and apply a softmax function to obtain the weights on the values.
Attention(Q, K, V) = softmax(Q * K^T / sqrt(dk)) * V

2.2 Multi-Head Attention
Instead of performing a single attention function with dmodel-dimensional queries, keys and values, we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections to dq, dk and dv dimensions, respectively.
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W^O
where head_i = Attention(Q * W_i^Q, K * W_i^K, V * W_i^V)

3. Training & Results
On the WMT 2014 English-to-German translation task, the big transformer model achieves a BLEU score of 28.4, outperforming the existing best models by over 2.0 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8.
"""
    },
    {
        "title": "Deep Residual Learning for Image Recognition (ResNet)",
        "filename": "deep_residual_learning_resnet.txt",
        "summary_short": "Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.",
        "content": """Title: Deep Residual Learning for Image Recognition
Authors: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
Published: 2016 (CVPR 2016 Best Paper)
Identifier: arXiv:1512.03385 / DOI:10.1109/CVPR.2016.90

Abstract:
Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth.

1. Introduction
Deep convolutional neural networks have led to a series of breakthroughs for image classification. Driven by the significance of depth, a question arises: Is learning better networks as easy as stacking more layers? An obstacle to answering this question was the notorious problem of vanishing/exploding gradients. When deeper networks are able to start converging, a degradation problem has been exposed: with network depth increasing, accuracy gets saturated and then degrades rapidly.

2. Residual Learning Framework
Instead of hoping every few stacked layers directly fit a desired underlying mapping H(x), we explicitly let these layers fit a residual mapping F(x) := H(x) - x. The original mapping is recast into F(x) + x. We hypothesize that it is easier to optimize the residual mapping than to optimize the original, unreferenced mapping.
The formulation F(x) + x can be realized by feedforward neural networks with "shortcut connections" (identity mappings).

3. Results on ImageNet and COCO
On the ImageNet classification dataset, we evaluate residual nets with a depth of up to 152 layers—8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task.
"""
    },
    {
        "title": "Quantum Approximate Optimization Algorithm (QAOA) for Combinatorial Problems",
        "filename": "qaoa_combinatorial_optimization.txt",
        "summary_short": "We introduce a quantum algorithm that produces approximations to combinatorial optimization problems based on alternating quantum operators on quantum states.",
        "content": """Title: A Quantum Approximate Optimization Algorithm
Authors: Edward Farhi, Jeffrey Goldstone, Sam Gutmann
Published: 2014 (arXiv:1411.4028)
Identifier: arXiv:1411.4028

Abstract:
We introduce a quantum algorithm that produces approximations to combinatorial optimization problems. The algorithm depends on an integer parameter p >= 1 and the quality of the approximation improves as p increases. The algorithm consists of applying a sequence of quantum gates characterized by 2p continuous parameters, followed by measurement in the computational basis.

1. Introduction & Problem Formulation
Combinatorial optimization problems involve finding an n-bit binary string z = z1...zn that maximizes a cost function C(z). We promote C(z) to a diagonal quantum Hamiltonian H_C in the computational basis. We also define a driver Hamiltonian H_B = sum_i X_i consisting of Pauli-X operators acting on individual qubits.

2. Variational Quantum State Preparation
Starting from the uniform superposition state |+>^n, we alternate between applying the problem Hamiltonian and the mixer Hamiltonian:
|gamma, beta> = U(B, beta_p) U(C, gamma_p) ... U(B, beta_1) U(C, gamma_1) |+>^n
where U(C, gamma) = exp(-i * gamma * H_C) and U(B, beta) = exp(-i * beta * H_B).

3. Parameter Optimization & Approximation Bounds
The expected value <gamma, beta| H_C |gamma, beta> is optimized over parameters (gamma, beta) using classical optimization techniques (such as Nelder-Mead, COBYLA, or gradient-based methods). For MaxCut on 3-regular graphs at p=1, the algorithm achieves an approximation ratio of at least 0.6924.
"""
    },
    {
        "title": "Denoising Diffusion Probabilistic Models (DDPM)",
        "filename": "denoising_diffusion_models.txt",
        "summary_short": "We present high quality image synthesis results using diffusion probabilistic models, a class of latent variable models inspired by non-equilibrium thermodynamics.",
        "content": """Title: Denoising Diffusion Probabilistic Models
Authors: Jonathan Ho, Ajay Jain, Pieter Abbeel
Published: 2020 (NeurIPS 2020)
Identifier: arXiv:2006.11239

Abstract:
We present high quality image synthesis results using diffusion probabilistic models, a class of latent variable models inspired by considerations from non-equilibrium thermodynamics. Our best results are obtained by training on a weighted variational bound designed according to a novel connection between diffusion probabilistic models and denoising score matching with Langevin dynamics.

1. Forward and Reverse Diffusion Processes
A diffusion model is a parameterized Markov chain trained using variational inference to produce samples matching the data after finite time.
- Forward process q(x_1:T | x_0): Gradually adds Gaussian noise according to a variance schedule beta_1, ..., beta_T.
  q(x_t | x_{t-1}) = N(x_t; sqrt(1 - beta_t) * x_{t-1}, beta_t * I)
- Reverse process p_theta(x_0:T): Learns to reverse the noise addition process using a neural network (typically a U-Net with attention).
  p_theta(x_{t-1} | x_t) = N(x_{t-1}; mu_theta(x_t, t), Sigma_theta(x_t, t))

2. Simplified Training Objective
We found that training the model to predict the injected noise epsilon rather than the clean mean yields significantly higher sample quality.
L_simple(theta) = E_{t, x_0, epsilon} [ || epsilon - epsilon_theta(sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * epsilon, t) ||^2 ]

3. High-Fidelity Generative Results
On unconditional CIFAR-10, our model achieves an Inception Score of 9.46 and a state-of-the-art FID score of 3.17. On 256x256 LSUN, we obtain sample quality competitive with ProgressiveGAN.
"""
    }
]

def seed():
    print("==================================================")
    print("  ScholarPulse AI Studio - Demo Data Seeding")
    print("==================================================")

    # 1. Create or get default demo researcher user
    user, created = User.objects.get_or_create(
        username='MCA_Evaluator',
        defaults={'email': 'evaluator@scholarpulse.ai', 'first_name': 'Lead', 'last_name': 'Researcher'}
    )
    if created:
        user.set_password('Research@2026')
        user.save()
        print(f"Created demo user: {user.username}")
    else:
        print(f"Demo user already exists: {user.username}")

    # Ensure profile exists
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.academic_level = 'MCA Student'
    profile.avatar = 'technomancer'
    profile.research_interests = 'Deep Learning, Quantum Optimization, Generative Diffusion, Transformers'
    profile.save()

    # 2. Seed documents
    seeded_docs = []
    for paper in PAPERS:
        doc = Document.objects.filter(title=paper["title"]).first()
        if not doc:
            content_bytes = paper["content"].strip().encode('utf-8')
            content_file = ContentFile(content_bytes, name=paper["filename"])
            doc = Document.objects.create(
                user=user,
                title=paper["title"],
                file=content_file,
                extracted_text=paper["content"].strip(),
                summary=paper["summary_short"],
                summary_short=paper["summary_short"]
            )
            print(f"Created Document ID {doc.id}: {doc.title}")

            # Store vectors
            try:
                chunks = chunk_text(paper["content"])
                store_document_chunks(doc.id, chunks)
                print(f"  -> Generated & stored {len(chunks)} vector chunks for Document ID {doc.id}")
            except Exception as e:
                print(f"  -> Vector store note: {e}")
        else:
            print(f"Document already exists: {doc.title} (ID: {doc.id})")
        seeded_docs.append(doc)

    # 3. Seed Sample Chat History for the first paper
    if seeded_docs:
        first_doc = seeded_docs[0]
        if not ChatHistory.objects.filter(document=first_doc).exists():
            ChatHistory.objects.create(
                document=first_doc,
                user=user,
                question="What is the core mathematical formulation of Scaled Dot-Product Attention?",
                answer="Scaled Dot-Product Attention is formulated as:\n\n$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$\n\nWhere $Q$, $K$, and $V$ denote Queries, Keys, and Values, and $d_k$ is the dimensionality of the key vectors."
            )
            print("  -> Seeded sample RAG conversation history.")

    print("==================================================")
    print("  Data Seeding Complete! Total Documents:", Document.objects.count())
    print("==================================================")

if __name__ == '__main__':
    seed()
