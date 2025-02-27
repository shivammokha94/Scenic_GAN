#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 21:55:47 2020

@author: smokha
"""

#conda activate tf15 before run



import torch
import torchvision
import torch.nn as nn #All NN modules, nn.Linear, nn.Conv2d, BatchNorm, Loss functions
import torch.optim as optim #For all optimizations alogrithms SGD, Adam
import torchvision.datasets as datasets #Standard datasets we can import
import torchvision.transforms as transforms #Transformation we can perform on datasets
from torch.utils.data import DataLoader #Fives easier dataset management and creates mini batches
from torch.utils.tensorboard import SummaryWriter #To print tensorboard
from model_utils import Discriminator, Generator #Import our models we've defined




#Hyperparameters


lr = 0.0005

batch_size = 64
image_size = 64   #MNIST 28 by 28 to 64 by 64
channels_img = 1
channels_noise = 256
num_epochs = 10

features_d = 16    #Use 64
features_g = 16    #Use 64


my_transforms = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
        ])

dataset = datasets.MNIST(root="dataset/", train=True, transform=my_transforms, download=True)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


#Create discriminator and generator

netD = Discriminator(channels_img, features_d).to(device)
netG = Generator(channels_noise, channels_img, features_g).to(device)


#Setup optimizer for G and D

optimizerD = optim.Adam(netD.parameters(), lr=lr, betas=(0.5, 0.999))
optimizerG = optim.Adam(netG.parameters(), lr=lr, betas=(0.5, 0.999))

netG.train()
netD.train()

criterion = nn.BCELoss()

real_label = 1
fake_label = 0

fixed_noise = torch.randn(64, channels_noise, 1, 1).to(device)
writer_real = SummaryWriter(f'runs/GAN_MNIST.test_real')
writer_fake = SummaryWriter(f'runs/GAN_MNIST.test_fake')
step = 0

print("Start training")

for epoch in range(num_epochs):
    
    for batch_idx, (data, targets) in enumerate(dataloader):
        
        data = data.to(device)
        batch_size = data.shape[0]
        
        #Train discriminator ---> max log(D(x)) + log(1-D(G(z)))
        netD.zero_grad()
        label = (torch.ones(batch_size)*0.9).to(device)
        output = netD(data).reshape(-1)    #Reshape to vector
        lossD_real = criterion(output, label)
        D_x = output.mean().item()
        
        
        noise = torch.randn(batch_size, channels_noise, 1, 1).to(device)
        fake = netG(noise)
        label = ((torch.ones(batch_size)*0.1)).to(device)
        
        
        output = netD(fake.detach()).reshape(-1)
        lossD_fake = criterion(output, label)
        
        lossD = lossD_real+lossD_fake
        lossD.backward()
        optimizerD.step()
        
        
        #Train generator ---> max log(d(G(z)))
        netG.zero_grad()
        label = torch.ones(batch_size).to(device)
        output = netD(fake).reshape(-1)
        lossG = criterion(output, label)
        lossG.backward()
        optimizerG.step()
        
        
        if batch_idx % 100 == 0:
            print(f'Epoch [{epoch}/{num_epochs}] Batch {batch_idx}/{len(dataloader)} LossD: {lossD: .4f}, LossG: {lossG: .4f} D(x): {D_x: .4f}')
            
            
            
            with torch.no_grad():
                fake = netG(fixed_noise)
                
                img_grid_real = torchvision.utils.make_grid(data[:32], normalize = True)
                img_grid_fake = torchvision.utils.make_grid(fake[:32], normalize = True)
                writer_real.add_image('MNIST Real Images', img_grid_real)
                writer_fake.add_image('MNIST Fake Images', img_grid_fake)
                
                
                
        
        
        
        
        