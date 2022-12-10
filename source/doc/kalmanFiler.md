
# Kalman Filter

The Kalman Filter is a numerical tool to estimate parameters. It uses statistical information and a state space model to estimate the upcoming state and update own model. It requires frequent updates about the real state with their uncertainty. This is the update step. In the predict step, the Kalman Filter receives the step parameter (in most cases time) and create a prediction. It also calculates it's uncertainty.

## Table of Contents

- [Kalman Filter](#kalman-filter)
  - [Table of Contents](#table-of-contents)
- [1. Prediction](#1-prediction)
- [2. Update](#2-update)
- [3. Used State Space Model and Observation Model](#3-used-state-space-model-and-observation-model)
  - [3.1. State Space](#31-state-space)
  - [3.2. Observation and Update](#32-observation-and-update)
 

# 1. Prediction

The following equations are used for the prediction step.
 
 $$ x_{k+1|k} = F \cdot x_{k|k} + G \cdot u_k $$
 $$ P_{k+1|k} = F \cdot P_{k|k} \cdot F^T + G\cdot Q_k \cdot G^T $$

 $x$ is the state vector, $F$ is the state model, $G$ the control matrice and $u$ the input vector.

 $P$ describes the uncertainty of the model state with the variance on the diagonal and the covariance the rest. $Q$ describes the variance and covariance of the input values and their interconnection to the watched state variable. Are the variances of each input parameter the same and not interconnected to the state parameters, than the equation $G \cdot Q_k \cdot G^T$ can be replaced by $G \cdot G^T \cdot \sigma^2$

$Q$ is defined as follows:

 $$ Q = \begin{bmatrix}\sigma^2_1 & \sigma_1\cdot\sigma_2 & \cdots & \sigma_1\cdot\sigma_n \\
 \sigma_2\cdot\sigma_1 & \sigma^2_2 & \cdots & \sigma_2\cdot\sigma_n \\
 \vdots & \vdots & \ddots & \vdots \\
 \sigma_m\cdot\sigma_1 & \sigma_m\cdot\sigma_2 & \cdots & \sigma^2_m
  \end{bmatrix}$$

  $P$ has the same definition with the size of the state space

Shapes for the State Space
  $$ x \in \mathbb{R^{m\times 1}}$$
  $$ F \in \mathbb{R^{m\times m}}$$
  $$ u \in \mathbb{R^{n\times 1}}$$
  $$ G \in \mathbb{R^{m\times n}}$$
  Shapes for the Covariance Equation:
  $$ P \in \mathbb{R^{m\times m}}$$
  $$ Q \in \mathbb{R^{n\times n}}$$
  
  # 2. Update

  In the update step, the Kalman filter receives the measured parameters and it's certainity and update the state space vector. To do so, it calculate on basis of the certainity the Kalman gain $K$. It describes how much of the model and how much of the measured values are taken to update the state space vector and lies between $K \in [0; 1]$.

  The update equations are as follows:

  $$y_k=m_k - H\cdot x_{k|k}$$
  $$S_k=H\cdot P_{k|k} \cdot H^T + R_k$$
  $$K_k=P_{k|k} \cdot H^T \cdot S_k^{-1}$$
  $$x_{k|k+1}=x_{k|k} + K_k \cdot y_k$$
  $$P_{k|k+1}=(I - K_k \cdot H) \cdot P_{k|k}$$

  **Sidenote: the update equation for P is the simplified version and is unstable in certain cases. The full equation is as follows:*

$$P_{k|k+1}=(I - K_k \cdot H) \cdot P_{k|k} \cdot (I - K_k \cdot H)^T + K_k\cdot R_k \cdot K_k^T$$

  Let's begin with the first equation. $y$ is the state space output exposed to the outside as difference or fit. Other than at the normal state space output equation with $y = C \cdot x+D\cdot u$, describes this equation the difference of the observed state space with it's noisy measured values $m$.
  
   $S$ desribes the covariance fit of the state space model and measurement noise. $R$ is the covariance matrice of the measurment.
   
   $K$ is the Kalman gain, which is used to determine the influence of the measurement on the state space vector and covariance matrice. $K$ controls if just the current state space and covariance matrice are kept of if they are updated by the difference/fit $y$.

   The shape are as follows:

   $$m\in \mathbb{R^{p\times 1}}$$
   $$R\in \mathbb{R^{p\times p}}$$
   $$y\in \mathbb{R^{p\times 1}}$$
   $$H\in \mathbb{R^{p\times m}}$$
   $$S\in \mathbb{R^{p\times p}}$$
   $$K\in \mathbb{R^{m\times p}}$$
   $$I\in \mathbb{R^{m\times m}}$$

   # 3. Used State Space Model and Observation Model

   As used state space vector, following parameters are used. Position x, velocity v and acceleration a for all three dimensions. Position x, y and z are measured and as control input, acceleration a is used.
   
   ## 3.1. State Space

   Their equations are:
   $$x = x_0+ v_0\cdot\Delta t + \frac{1}{2}\cdot\Delta t \cdot a$$
   $$v = v_0 + \Delta t \cdot a$$
   $$a = a$$

   To describe it in all three dimensions x, y, z and as matrix system leads to the following matrices:

   $$x= \begin{bmatrix}x\\y\\z\\v_x\\v_y\\v_z\\a_x\\a_y\\a_z\end{bmatrix}$$

   $$F= \begin{bmatrix}
   1 & 0 & 0 & \Delta t & 0 & 0 & 0 & 0 & 0 \\
   0 & 1 & 0 & 0 & \Delta t & 0 & 0 & 0 & 0 \\
   0 & 0 & 1 & 0 & 0 & \Delta t & 0 & 0 & 0 \\
   0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0\\
   0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0\\
   0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0\\
   0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
   0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
   0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0
    \end{bmatrix}$$

   For the system input follows:

   $$u= \begin{bmatrix}a_x\\a_y\\a_z\end{bmatrix}$$

   $$G= \begin{bmatrix}
   \frac{1}{2}\cdot\Delta t & 0 & 0\\
   0 & \frac{1}{2}\cdot\Delta t & \\
   0 & 0 & \frac{1}{2}\cdot\Delta t \\
   \Delta t & 0 & 0 \\
   0 & \Delta t & 0 \\
   0 & 0 & \Delta t \\
   1 & 0 & 0 \\
   0 & 1 & 0 \\
   0 & 0 & 1 
    \end{bmatrix}$$

   Trough that, that all dimension are watched seperately, there is no interconnection to the other and the covariance matrice is simply a diagonal matrice with the variances. 

   $$Q= \begin{bmatrix}
   \sigma_{ax}^2 & 0 & 0\\
   0 & \sigma_{ay}^2 & 0 \\
   0 & 0 & \sigma_{az}^2 \\
    \end{bmatrix}$$

   ## 3.2. Observation and Update

   $$m = \begin{bmatrix} x\\ y\\ z\end{bmatrix} $$
   $$R = \begin{bmatrix}
    \sigma_{x}^2 & 0 & 0\\
    0 & \sigma_{y}^2 & 0\\
    0 & 0 &\sigma_{z}^2\\
   \end{bmatrix} $$

   $y$ is directly connected to the measured variables and has the same shape as $m$.

   $$H = \begin{bmatrix}
   1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
   0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0\\
   0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0\\
   \end{bmatrix}$$