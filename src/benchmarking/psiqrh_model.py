#!/usr/bin/env python3
"""
CollTech-AGI ΨQRH (Quaternion + Spectral + Fractal + Leech Lattice) Transformer Model

Advanced transformer architecture that integrates:
- Quaternion attention mechanisms
- Spectral processing layers
- Fractal neural structures
- Leech lattice embeddings

This model is designed to work seamlessly with the CollTech-AGI consciousness system.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PsiQRHConfig:
    """Configuration for ΨQRH Transformer model."""
    # Model dimensions
    vocab_size: int = 50257
    d_model: int = 768
    n_heads: int = 12
    n_layers: int = 12
    d_ff: int = 3072
    max_seq_len: int = 2048
    
    # ΨQRH specific parameters
    quaternion_dim: int = 4
    spectral_layers: int = 3
    fractal_depth: int = 4
    leech_lattice_dim: int = 24
    
    # Training parameters
    dropout: float = 0.1
    activation: str = "gelu"
    layer_norm_eps: float = 1e-5
    
    # Consciousness integration
    consciousness_aware: bool = True
    memory_integration: bool = True
    drift_resistant: bool = True


class QuaternionAttention(nn.Module):
    """
    Quaternion-based attention mechanism.
    
    Uses quaternion algebra for more expressive attention computations
    that can capture complex relationships in the data.
    """
    
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        # Quaternion components (w, x, y, z)
        self.q_linear = nn.Linear(d_model, d_model * 4)  # 4 components
        self.k_linear = nn.Linear(d_model, d_model * 4)
        self.v_linear = nn.Linear(d_model, d_model * 4)
        self.out_linear = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(self.d_k)
    
    def quaternion_multiply(self, q1: torch.Tensor, q2: torch.Tensor) -> torch.Tensor:
        """Multiply two quaternions."""
        # q1, q2 shape: (batch, heads, seq_len, 4)
        w1, x1, y1, z1 = q1[..., 0], q1[..., 1], q1[..., 2], q1[..., 3]
        w2, x2, y2, z2 = q2[..., 0], q2[..., 1], q2[..., 2], q2[..., 3]
        
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        
        return torch.stack([w, x, y, z], dim=-1)
    
    def quaternion_norm(self, q: torch.Tensor) -> torch.Tensor:
        """Compute quaternion norm."""
        return torch.sqrt(torch.sum(q ** 2, dim=-1, keepdim=True))
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        batch_size, seq_len, _ = x.size()
        
        # Project to quaternion space
        q_quat = self.q_linear(x).view(batch_size, seq_len, self.n_heads, 4, self.d_k)
        k_quat = self.k_linear(x).view(batch_size, seq_len, self.n_heads, 4, self.d_k)
        v_quat = self.v_linear(x).view(batch_size, seq_len, self.n_heads, 4, self.d_k)
        
        # Transpose for attention computation
        q_quat = q_quat.transpose(1, 2)  # (batch, heads, seq_len, 4, d_k)
        k_quat = k_quat.transpose(1, 2)
        v_quat = v_quat.transpose(1, 2)
        
        # Compute quaternion attention scores
        # Use quaternion multiplication for more expressive attention
        scores = torch.zeros(batch_size, self.n_heads, seq_len, seq_len, device=x.device)
        
        for i in range(seq_len):
            for j in range(seq_len):
                # Quaternion multiplication between query and key
                qk_product = self.quaternion_multiply(q_quat[:, :, i], k_quat[:, :, j])
                # Use the real component (w) as attention score
                scores[:, :, i, j] = qk_product[:, :, 0].sum(dim=-1)
        
        scores = scores / self.scale
        
        # Apply mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Apply softmax
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # Apply attention to values
        # Convert quaternion values to real values for output
        v_real = v_quat[..., 0]  # Use real component
        context = torch.matmul(attn_weights, v_real)
        
        # Reshape and project back
        context = context.transpose(1, 2).contiguous().view(
            batch_size, seq_len, self.d_model
        )
        
        return self.out_linear(context)


class SpectralLayer(nn.Module):
    """
    Spectral processing layer using FFT-based transformations.
    
    Applies frequency domain processing to capture spectral patterns
    in the data that might be missed by standard attention mechanisms.
    """
    
    def __init__(self, d_model: int, dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.dropout = nn.Dropout(dropout)
        
        # Spectral transformation layers
        self.spectral_conv = nn.Conv1d(d_model, d_model, kernel_size=3, padding=1)
        self.spectral_norm = nn.LayerNorm(d_model)
        
        # Frequency domain processing
        self.freq_weights = nn.Parameter(torch.randn(d_model // 2 + 1))
        self.phase_weights = nn.Parameter(torch.randn(d_model // 2 + 1))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, d_model = x.size()
        
        # Apply spectral convolution
        x_conv = self.spectral_conv(x.transpose(1, 2)).transpose(1, 2)
        x_conv = self.spectral_norm(x_conv)
        
        # FFT-based processing
        x_fft = torch.fft.rfft(x_conv, dim=1)
        
        # Apply frequency and phase weights
        magnitude = torch.abs(x_fft)
        phase = torch.angle(x_fft)
        
        # Weighted frequency components
        weighted_magnitude = magnitude * self.freq_weights.unsqueeze(0).unsqueeze(-1)
        weighted_phase = phase + self.phase_weights.unsqueeze(0).unsqueeze(-1)
        
        # Reconstruct signal
        x_processed = torch.fft.irfft(
            weighted_magnitude * torch.exp(1j * weighted_phase),
            n=seq_len, dim=1
        )
        
        # Residual connection and dropout
        output = x + self.dropout(x_processed)
        return output


class FractalLayer(nn.Module):
    """
    Fractal neural layer that creates self-similar structures.
    
    Implements fractal-like neural patterns that can capture
    hierarchical and recursive patterns in the data.
    """
    
    def __init__(self, d_model: int, fractal_depth: int = 4, dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.fractal_depth = fractal_depth
        self.dropout = nn.Dropout(dropout)
        
        # Fractal structure layers
        self.fractal_layers = nn.ModuleList([
            nn.Linear(d_model, d_model) for _ in range(fractal_depth)
        ])
        
        # Scaling factors for fractal structure
        self.scale_factors = nn.Parameter(torch.ones(fractal_depth))
        
        # Fractal combination weights
        self.combination_weights = nn.Parameter(torch.ones(fractal_depth))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        fractal_outputs = []
        
        # Apply fractal layers with different scales
        for i, layer in enumerate(self.fractal_layers):
            # Scale the input
            scaled_input = x * self.scale_factors[i]
            
            # Apply layer
            layer_output = layer(scaled_input)
            
            # Apply activation
            layer_output = F.gelu(layer_output)
            
            fractal_outputs.append(layer_output)
        
        # Combine fractal outputs
        combined = torch.zeros_like(x)
        for i, output in enumerate(fractal_outputs):
            combined += self.combination_weights[i] * output
        
        # Normalize
        combined = combined / self.combination_weights.sum()
        
        # Residual connection
        output = x + self.dropout(combined)
        return output


class LeechLatticeEmbedding(nn.Module):
    """
    Leech lattice-based embedding layer.
    
    Uses the mathematical structure of the Leech lattice (24-dimensional)
    to create high-dimensional embeddings that capture complex relationships.
    """
    
    def __init__(self, vocab_size: int, d_model: int, leech_dim: int = 24):
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.leech_dim = leech_dim
        
        # Standard embedding
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        # Leech lattice projection
        self.leech_projection = nn.Linear(d_model, leech_dim)
        self.leech_inverse = nn.Linear(leech_dim, d_model)
        
        # Leech lattice basis (simplified)
        self.register_buffer('leech_basis', self._generate_leech_basis())
    
    def _generate_leech_basis(self) -> torch.Tensor:
        """Generate a simplified Leech lattice basis."""
        # This is a simplified version - real Leech lattice is more complex
        basis = torch.randn(self.leech_dim, self.leech_dim)
        # Orthogonalize
        basis = torch.linalg.qr(basis)[0]
        return basis
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Standard embedding
        embedded = self.embedding(x)
        
        # Project to Leech lattice space
        leech_proj = self.leech_projection(embedded)
        
        # Apply Leech lattice transformation
        leech_transformed = torch.matmul(leech_proj, self.leech_basis)
        
        # Project back to model dimension
        output = self.leech_inverse(leech_transformed)
        
        return output


class PsiQRHTransformerBlock(nn.Module):
    """
    Complete ΨQRH Transformer block combining all components.
    """
    
    def __init__(self, config: PsiQRHConfig):
        super().__init__()
        self.config = config
        
        # Quaternion attention
        self.quaternion_attention = QuaternionAttention(
            config.d_model, config.n_heads, config.dropout
        )
        
        # Spectral layer
        self.spectral_layer = SpectralLayer(config.d_model, config.dropout)
        
        # Fractal layer
        self.fractal_layer = FractalLayer(
            config.d_model, config.fractal_depth, config.dropout
        )
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.norm2 = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.norm3 = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        
        # Feed-forward network
        self.ffn = nn.Sequential(
            nn.Linear(config.d_model, config.d_ff),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.d_ff, config.d_model),
            nn.Dropout(config.dropout)
        )
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        # Quaternion attention with residual connection
        attn_output = self.quaternion_attention(x, mask)
        x = self.norm1(x + attn_output)
        
        # Spectral processing
        spectral_output = self.spectral_layer(x)
        x = self.norm2(spectral_output)
        
        # Fractal processing
        fractal_output = self.fractal_layer(x)
        x = self.norm3(fractal_output)
        
        # Feed-forward network
        ffn_output = self.ffn(x)
        x = x + ffn_output
        
        return x


class PsiQRHModel(nn.Module):
    """
    Complete ΨQRH Transformer model.
    
    Integrates quaternion attention, spectral processing, fractal layers,
    and Leech lattice embeddings into a cohesive transformer architecture.
    """
    
    def __init__(self, config: PsiQRHConfig):
        super().__init__()
        self.config = config
        
        # Embeddings
        self.token_embedding = LeechLatticeEmbedding(
            config.vocab_size, config.d_model, config.leech_lattice_dim
        )
        self.position_embedding = nn.Embedding(config.max_seq_len, config.d_model)
        
        # Transformer blocks
        self.transformer_blocks = nn.ModuleList([
            PsiQRHTransformerBlock(config) for _ in range(config.n_layers)
        ])
        
        # Output layers
        self.ln_f = nn.LayerNorm(config.d_model, eps=config.layer_norm_eps)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        
        # Initialize weights
        self.apply(self._init_weights)
        
        logger.info(f"ΨQRH Model initialized with {config.n_layers} layers")
        logger.info(f"Model dimension: {config.d_model}, Heads: {config.n_heads}")
    
    def _init_weights(self, module):
        """Initialize model weights."""
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, nn.LayerNorm):
            torch.nn.init.zeros_(module.bias)
            torch.nn.init.ones_(module.weight)
    
    def forward(self, input_ids: torch.Tensor, attention_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        batch_size, seq_len = input_ids.size()
        
        # Create position indices
        position_ids = torch.arange(seq_len, device=input_ids.device).unsqueeze(0)
        
        # Token and position embeddings
        token_embeds = self.token_embedding(input_ids)
        position_embeds = self.position_embedding(position_ids)
        x = token_embeds + position_embeds
        
        # Create attention mask
        if attention_mask is None:
            attention_mask = torch.ones(batch_size, seq_len, device=input_ids.device)
        
        # Apply transformer blocks
        for block in self.transformer_blocks:
            x = block(x, attention_mask)
        
        # Final layer norm and output projection
        x = self.ln_f(x)
        logits = self.lm_head(x)
        
        return logits
    
    def generate(self, input_ids: torch.Tensor, max_length: int = 100, 
                temperature: float = 1.0, top_k: int = 50, top_p: float = 0.9) -> torch.Tensor:
        """Generate text using the model."""
        self.eval()
        
        with torch.no_grad():
            for _ in range(max_length - input_ids.size(1)):
                # Get logits for the last token
                logits = self.forward(input_ids)
                next_token_logits = logits[:, -1, :] / temperature
                
                # Apply top-k filtering
                if top_k > 0:
                    top_k_logits, top_k_indices = torch.topk(next_token_logits, top_k)
                    next_token_logits = torch.full_like(next_token_logits, -float('inf'))
                    next_token_logits.scatter_(1, top_k_indices, top_k_logits)
                
                # Apply top-p filtering
                if top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    
                    indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
                    next_token_logits[indices_to_remove] = -float('inf')
                
                # Sample next token
                probs = F.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                
                # Append to input
                input_ids = torch.cat([input_ids, next_token], dim=1)
        
        return input_ids
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            'model_type': 'PsiQRH_Transformer',
            'config': {
                'vocab_size': self.config.vocab_size,
                'd_model': self.config.d_model,
                'n_heads': self.config.n_heads,
                'n_layers': self.config.n_layers,
                'd_ff': self.config.d_ff,
                'max_seq_len': self.config.max_seq_len,
                'quaternion_dim': self.config.quaternion_dim,
                'spectral_layers': self.config.spectral_layers,
                'fractal_depth': self.config.fractal_depth,
                'leech_lattice_dim': self.config.leech_lattice_dim
            },
            'parameters': {
                'total': total_params,
                'trainable': trainable_params,
                'non_trainable': total_params - trainable_params
            },
            'consciousness_integration': {
                'consciousness_aware': self.config.consciousness_aware,
                'memory_integration': self.config.memory_integration,
                'drift_resistant': self.config.drift_resistant
            }
        }


def create_psiqrh_model(config: Optional[PsiQRHConfig] = None) -> PsiQRHModel:
    """Create a ΨQRH model with the given configuration."""
    if config is None:
        config = PsiQRHConfig()
    
    model = PsiQRHModel(config)
    logger.info("✅ ΨQRH Model created successfully")
    
    return model


def load_psiqrh_model(model_path: str, config: Optional[PsiQRHConfig] = None) -> PsiQRHModel:
    """Load a ΨQRH model from a checkpoint."""
    if config is None:
        config = PsiQRHConfig()
    
    model = PsiQRHModel(config)
    
    # Load checkpoint
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint['model_state_dict'])
    
    logger.info(f"✅ ΨQRH Model loaded from {model_path}")
    
    return model


if __name__ == "__main__":
    # Test the ΨQRH model
    print("🧠 Testing ΨQRH Transformer Model")
    print("=" * 50)
    
    # Create model
    config = PsiQRHConfig(
        vocab_size=1000,
        d_model=256,
        n_heads=8,
        n_layers=6,
        max_seq_len=512
    )
    
    model = create_psiqrh_model(config)
    
    # Test forward pass
    batch_size = 2
    seq_len = 128
    input_ids = torch.randint(0, config.vocab_size, (batch_size, seq_len))
    
    print(f"Input shape: {input_ids.shape}")
    
    # Forward pass
    logits = model(input_ids)
    print(f"Output shape: {logits.shape}")
    
    # Test generation
    print("\n🎯 Testing text generation...")
    prompt = torch.randint(0, config.vocab_size, (1, 10))
    generated = model.generate(prompt, max_length=50, temperature=0.8)
    print(f"Generated sequence length: {generated.shape[1]}")
    
    # Model info
    info = model.get_model_info()
    print(f"\n📊 Model Information:")
    print(f"   Total parameters: {info['parameters']['total']:,}")
    print(f"   Trainable parameters: {info['parameters']['trainable']:,}")
    print(f"   Model dimension: {info['config']['d_model']}")
    print(f"   Number of layers: {info['config']['n_layers']}")
    print(f"   Number of heads: {info['config']['n_heads']}")
    
    print("\n✅ ΨQRH Model test completed!")
