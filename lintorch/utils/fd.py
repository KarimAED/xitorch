# This file contains calculation of finite differences for debugging purposes
import torch

def finite_differences(fcn, args, iarg, eps=1e-6):
    with torch.no_grad():
        nelmt = args[iarg].numel()
        shape = args[iarg].shape
        device = args[iarg].device
        dxs = torch.eye(nelmt).to(device) * eps

        loss0 = fcn(*args)
        dlossdx = torch.empty(nelmt).to(args[iarg].dtype).to(device)
        for i in range(nelmt):
            newarg = args[iarg].detach() + dxs[i,:].view(shape)
            newargs = [(args[j] if j != iarg else newarg) for j in range(len(args))]
            loss = fcn(*newargs)
            dlossdx[i] = (loss - loss0) / eps

        return dlossdx.view(shape)
