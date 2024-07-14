import os
import torch
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torchvision.utils import save_image
from models import Generator, Discriminator
import torch.nn as nn

# Hyperparameters
batch_size = 64
lr = 0.0002
z_dim = 100
image_size = 64
epochs = 200

# Transformations
transform = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# Dataset and DataLoader
dataset = datasets.ImageFolder(root='dataset', transform=transform)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize models
gen = Generator(z_dim).cuda()
disc = Discriminator(1).cuda()

# Optimizers
opt_gen = optim.Adam(gen.parameters(), lr=lr, betas=(0.5, 0.999))
opt_disc = optim.Adam(disc.parameters(), lr=lr, betas=(0.5, 0.999))

# Loss
criterion = nn.BCELoss()

# Training Loop
for epoch in range(epochs):
    for batch_idx, (real, _) in enumerate(dataloader):
        real = real.cuda()
        noise = torch.randn(batch_size, z_dim, 1, 1).cuda()
        fake = gen(noise)

        # Train Discriminator
        disc_real = disc(real).view(-1)
        lossD_real = criterion(disc_real, torch.ones_like(disc_real))
        disc_fake = disc(fake.detach()).view(-1)
        lossD_fake = criterion(disc_fake, torch.zeros_like(disc_fake))
        lossD = (lossD_real + lossD_fake) / 2
        disc.zero_grad()
        lossD.backward()
        opt_disc.step()

        # Train Generator
        output = disc(fake).view(-1)
        lossG = criterion(output, torch.ones_like(output))
        gen.zero_grad()
        lossG.backward()
        opt_gen.step()

        if batch_idx % 100 == 0:
            print(f"Epoch [{epoch}/{epochs}] Batch {batch_idx}/{len(dataloader)} \
                  Loss D: {lossD:.4f}, loss G: {lossG:.4f}")
            with torch.no_grad():
                fake = gen(noise)
                save_image(fake * 0.5 + 0.5, f"output/{epoch}_{batch_idx}.png")
