"""
Instruction:

In this section, you are asked to train a NN with different hyperparameters.
To start with training, you need to fill in the incomplete code. There are 3
places that you need to complete:
a) Backward pass equations for an affine layer (linear transformation + bias).
b) Backward pass equations for ReLU activation function.
c) Weight update equations with momentum.

After correctly fill in the code, modify the hyperparameters in "main()".
You can then run this file with the command: "python nn.py" in your terminal.
The program will automatically check your gradient implementation before start.
The program will print out the training progress, and it will display the
training curve by the end. You can optionally save the model by uncommenting
the lines in "main()".
"""

from __future__ import division
from __future__ import print_function

from util import LoadData, Load, Save, DisplayPlot
import sys
import numpy as np


def InitNN(num_inputs, num_hiddens, num_outputs):
    """Initializes NN parameters.

    Args:
        num_inputs:    Number of input units.
        num_hiddens:   List of two elements, hidden size for each layer.
        num_outputs:   Number of output units.

    Returns:
        model:         Randomly initialized network weights.
    """
    W1 = 0.1 * np.random.randn(num_inputs, num_hiddens[0])
    W2 = 0.1 * np.random.randn(num_hiddens[0], num_hiddens[1])
    W3 = 0.01 * np.random.randn(num_hiddens[1], num_outputs)
    b1 = np.zeros((num_hiddens[0]))
    b2 = np.zeros((num_hiddens[1]))
    b3 = np.zeros((num_outputs))
    model = {
        'W1': W1,
        'W2': W2,
        'W3': W3,
        'b1': b1,
        'b2': b2,
        'b3': b3
    }
    return model


def Affine(x, w, b):
    """Computes the affine transformation.

    Args:
        x: Inputs
        w: Weights
        b: Bias

    Returns:
        y: Outputs
    """
    # y = np.dot(w.T, x) + b
    y = x.dot(w) + b
    return y


def AffineBackward(grad_y, x, w):
    """Computes gradients of affine transformation.

    Args:
        grad_y: gradient from last layer
        x: inputs
        w: weights

    Returns:
        grad_x: Gradients wrt. the inputs.
        grad_w: Gradients wrt. the weights.
        grad_b: Gradients wrt. the biases.
    """
    ###########################
    # Insert your code here.
    # grad_x = ...
    # grad_w = ...
    # grad_b = ...
    # return grad_x, grad_w, grad_b
    ###########################

    grad_x = np.dot(grad_y, w.T)
    grad_w = np.dot(x.T, grad_y)
    grad_b = np.sum(grad_y, axis=0)
    return grad_x, grad_w, grad_b

    # raise Exception('Not implemented')



def ReLU(x):
    """Computes the ReLU activation function.

    Args:
        x: Inputs

    Returns:
        y: Activation
    """
    return np.maximum(x, 0.0)


def ReLUBackward(grad_y, x, y):
    """Computes gradients of the ReLU activation function.

    Returns:
        grad_x: Gradients wrt. the inputs.
    """
    ###########################
    # Insert your code here.
    # grad_x = ...
    # return grad_x
    ###########################

    return grad_y * (x > 0)

    # raise Exception('Not implemented')


def Softmax(x):
    """Computes the softmax activation function.

    Args:
        x: Inputs

    Returns:
        y: Activation
    """
    return np.exp(x) / np.exp(x).sum(axis=1, keepdims=True)


def NNForward(model, x):
    """Runs the forward pass.

    Args:
        model: Dictionary of all the weights.
        x:     Input to the network.

    Returns:
        var:   Dictionary of all intermediate variables.
    """
    h1 = Affine(x, model['W1'], model['b1'])
    h1r = ReLU(h1)
    h2 = Affine(h1r, model['W2'], model['b2'])
    h2r = ReLU(h2)
    y = Affine(h2r, model['W3'], model['b3'])
    var = {
        'x': x,
        'h1': h1,
        'h1r': h1r,
        'h2': h2,
        'h2r': h2r,
        'y': y
    }
    return var


def NNBackward(model, err, var):
    """Runs the backward pass.

    Args:
        model:    Dictionary of all the weights.
        err:      Gradients to the output of the network.
        var:      Intermediate variables from the forward pass.
    """
    dE_dh2r, dE_dW3, dE_db3 = AffineBackward(err, var['h2r'], model['W3'])
    dE_dh2 = ReLUBackward(dE_dh2r, var['h2'], var['h2r'])
    dE_dh1r, dE_dW2, dE_db2 = AffineBackward(dE_dh2, var['h1r'], model['W2'])
    dE_dh1 = ReLUBackward(dE_dh1r, var['h1'], var['h1r'])
    _, dE_dW1, dE_db1 = AffineBackward(dE_dh1, var['x'], model['W1'])
    model['dE_dW1'] = dE_dW1
    model['dE_dW2'] = dE_dW2
    model['dE_dW3'] = dE_dW3
    model['dE_db1'] = dE_db1
    model['dE_db2'] = dE_db2
    model['dE_db3'] = dE_db3
    pass


def NNUpdate(model, eps, momentum):
    """Update NN weights.

    Args:
        model:    Dictionary of all the weights.
        eps:      Learning rate.
        momentum: Momentum.
    """
    ###########################
    # Insert your code here.
    # Update the weights.
    # model['W1'] = ...
    # model['W2'] = ...
    # model['W3'] = ...
    # model['b1'] = ...
    # model['b2'] = ...
    # model['b3'] = ...
    ###########################

    velocity_w1 = np.zeros(model['W1'].shape)
    velocity_w2 = np.zeros(model['W2'].shape)
    velocity_w3 = np.zeros(model['W3'].shape)
    velocity_b1 = np.zeros(model['b1'].shape)
    velocity_b2 = np.zeros(model['b2'].shape)
    velocity_b3 = np.zeros(model['b3'].shape)

    model['W1'] = model["W1"] + ( momentum * velocity_w1 - eps * model['dE_dW1'] )
    model['W2'] = model['W2'] + ( momentum * velocity_w2 - eps * model['dE_dW2'] )
    model['W3'] = model['W3'] + ( momentum * velocity_w3 - eps * model['dE_dW3'] )
    model['b1'] = model['b1'] + ( momentum * velocity_b1 - eps * model['dE_db1'] )
    model['b2'] = model['b2'] + ( momentum * velocity_b2 - eps * model['dE_db2'] )
    model['b3'] = model['b3'] + ( momentum * velocity_b3 - eps * model['dE_db3'] )

    # raise Exception('Not implemented')


def Train(model, forward, backward, update, eps, momentum, num_epochs,
          batch_size):
    """Trains a simple MLP.

    Args:
        model:           Dictionary of model weights.
        forward:         Forward prop function.
        backward:        Backward prop function.
        update:          Update weights function.
        eps:             Learning rate.
        momentum:        Momentum.
        num_epochs:      Number of epochs to run training for.
        batch_size:      Mini-batch size, -1 for full batch.

    Returns:
        stats:           Dictionary of training statistics.
            - train_ce:       Training cross entropy.
            - valid_ce:       Validation cross entropy.
            - train_acc:      Training accuracy.
            - valid_acc:      Validation accuracy.
    """
    inputs_train, inputs_valid, inputs_test, target_train, target_valid, \
        target_test = LoadData('./toronto_face.npz')
    rnd_idx = np.arange(inputs_train.shape[0])
    train_ce_list = []
    valid_ce_list = []
    train_acc_list = []
    valid_acc_list = []
    num_train_cases = inputs_train.shape[0]
    if batch_size == -1:
        batch_size = num_train_cases
    num_steps = int(np.ceil(num_train_cases / batch_size))
    for epoch in range(num_epochs):
        np.random.shuffle(rnd_idx)
        inputs_train = inputs_train[rnd_idx]
        target_train = target_train[rnd_idx]
        for step in range(num_steps):
            # Forward prop.
            start = step * batch_size
            end = min(num_train_cases, (step + 1) * batch_size)
            x = inputs_train[start: end]
            t = target_train[start: end]

            var = forward(model, x)
            prediction = Softmax(var['y'])

            train_ce = -np.sum(t * np.log(prediction)) / x.shape[0]
            train_acc = (np.argmax(prediction, axis=1) ==
                         np.argmax(t, axis=1)).astype('float').mean()
            print(('Epoch {:3d} Step {:2d} Train CE {:.5f} '
                   'Train Acc {:.5f}').format(
                epoch, step, train_ce, train_acc))

            # Compute error.
            error = (prediction - t) / x.shape[0]

            # Backward prop.
            backward(model, error, var)

            # Update weights.
            update(model, eps, momentum)

        valid_ce, valid_acc = Evaluate(
            inputs_valid, target_valid, model, forward, batch_size=batch_size)
        print(('Epoch {:3d} '
               'Validation CE {:.5f} '
               'Validation Acc {:.5f}\n').format(
            epoch, valid_ce, valid_acc))
        train_ce_list.append((epoch, train_ce))
        train_acc_list.append((epoch, train_acc))
        valid_ce_list.append((epoch, valid_ce))
        valid_acc_list.append((epoch, valid_acc))
    DisplayPlot(train_ce_list, valid_ce_list, 'Cross Entropy', number=0)
    DisplayPlot(train_acc_list, valid_acc_list, 'Accuracy', number=1)

    print()
    train_ce, train_acc = Evaluate(
        inputs_train, target_train, model, forward, batch_size=batch_size)
    valid_ce, valid_acc = Evaluate(
        inputs_valid, target_valid, model, forward, batch_size=batch_size)
    test_ce, test_acc = Evaluate(
        inputs_test, target_test, model, forward, batch_size=batch_size)
    print('CE: Train %.5f Validation %.5f Test %.5f' %
          (train_ce, valid_ce, test_ce))
    print('Acc: Train {:.5f} Validation {:.5f} Test {:.5f}'.format(
        train_acc, valid_acc, test_acc))

    stats = {
        'train_ce': train_ce_list,
        'valid_ce': valid_ce_list,
        'train_acc': train_acc_list,
        'valid_acc': valid_acc_list
    }

    return model, stats


def Evaluate(inputs, target, model, forward, batch_size=-1):
    """Evaluates the model on inputs and target.

    Args:
        inputs: Inputs to the network.
        target: Target of the inputs.
        model:  Dictionary of network weights.
    """
    num_cases = inputs.shape[0]
    if batch_size == -1:
        batch_size = num_cases
    num_steps = int(np.ceil(num_cases / batch_size))
    ce = 0.0
    acc = 0.0
    for step in range(num_steps):
        start = step * batch_size
        end = min(num_cases, (step + 1) * batch_size)
        x = inputs[start: end]
        t = target[start: end]
        prediction = Softmax(forward(model, x)['y'])
        ce += -np.sum(t * np.log(prediction))
        acc += (np.argmax(prediction, axis=1) == np.argmax(
            t, axis=1)).astype('float').sum()
    ce /= num_cases
    acc /= num_cases
    return ce, acc


def CheckGrad(model, forward, backward, name, x):
    """Check the gradients

    Args:
        model: Dictionary of network weights.
        name: Weights name to check.
        x: Fake input.
    """
    np.random.seed(0)
    var = forward(model, x)
    loss = lambda y: 0.5 * (y ** 2).sum()
    grad_y = var['y']
    backward(model, grad_y, var)
    grad_w = model['dE_d' + name].ravel()
    w_ = model[name].ravel()
    eps = 1e-7
    grad_w_2 = np.zeros(w_.shape)
    check_elem = np.arange(w_.size)
    np.random.shuffle(check_elem)
    # Randomly check 20 elements.
    check_elem = check_elem[:20]
    for ii in check_elem:
        w_[ii] += eps
        err_plus = loss(forward(model, x)['y'])
        w_[ii] -= 2 * eps
        err_minus = loss(forward(model, x)['y'])
        w_[ii] += eps
        grad_w_2[ii] = (err_plus - err_minus) / 2 / eps
    np.testing.assert_almost_equal(grad_w[check_elem], grad_w_2[check_elem],
                                   decimal=3)


def main():
    """Trains a NN."""
    model_fname = 'toronto_face.npz'
    stats_fname = 'nn_stats.npz'

    # Hyper-parameters. Modify them if needed.
    num_hiddens = [90, 90]
    eps = 0.06
    momentum = 0.9
    num_epochs = 1000
    batch_size = 1000

    # Input-output dimensions.
    num_inputs = 2304
    num_outputs = 7


    # Initialize model.
    model = InitNN(num_inputs, num_hiddens, num_outputs)

    # Uncomment to reload trained model here.
    # model = Load(model_fname)

    # Check gradient implementation.
    print('Checking gradients...')
    x = np.random.rand(10, 48 * 48) * 0.1
    CheckGrad(model, NNForward, NNBackward, 'W3', x)
    CheckGrad(model, NNForward, NNBackward, 'b3', x)
    CheckGrad(model, NNForward, NNBackward, 'W2', x)
    CheckGrad(model, NNForward, NNBackward, 'b2', x)
    CheckGrad(model, NNForward, NNBackward, 'W1', x)
    CheckGrad(model, NNForward, NNBackward, 'b1', x)

    # Train model.
    stats = Train(model, NNForward, NNBackward, NNUpdate, eps,
                  momentum, num_epochs, batch_size)

    # Uncomment if you wish to save the model.
    # Save(model_fname, model)

    # Uncomment if you wish to save the training statistics.
    # Save(stats_fname, stats)

if __name__ == '__main__':
    main()
