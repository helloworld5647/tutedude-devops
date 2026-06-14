provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "backend" {
  name = "tutedude-backend"
}

resource "aws_ecr_repository" "frontend" {
  name = "tutedude-frontend"
}

# VPC

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "ecs-vpc"
  }
}


# INTERNET GATEWAY


resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}


# SUBNETS


resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
}


# ROUTE TABLE


resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    gateway_id = aws_internet_gateway.igw.id
    cidr_block = "0.0.0.0/0"
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}


# SECURITY GROUP


resource "aws_security_group" "ecs_sg" {

  name   = "ecs-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 3000
    to_port   = 3000
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 5000
    to_port   = 5000
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}


# ECS CLUSTER


resource "aws_ecs_cluster" "main" {
  name = "tutedude-cluster"
}

# BACKEND TASK


resource "aws_ecs_task_definition" "backend" {

  family = "backend"

  requires_compatibilities = ["FARGATE"]

  network_mode = "awsvpc"

  cpu    = "256"
  memory = "512"

  execution_role_arn = "arn:aws:iam::426449772516:role/ecsTaskExecutionRole"

  container_definitions = jsonencode([
    {
      name = "backend"

      image = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/tutedude-backend:latest"

      essential = true

      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
    }
  ])
}

# FRONTEND TASK


resource "aws_ecs_task_definition" "frontend" {

  family = "frontend"

  requires_compatibilities = ["FARGATE"]

  network_mode = "awsvpc"

  cpu    = "256"
  memory = "512"

  execution_role_arn = "arn:aws:iam::426449772516:role/ecsTaskExecutionRole"

  container_definitions = jsonencode([
    {
      name = "frontend"

      image = "${var.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/tutedude-frontend:latest"

      essential = true

      environment = [
        {
          name  = "BACKEND_URL"
          value = "http://10.0.1.215:5000 "
        }
      ]


      portMappings = [
        {
          containerPort = 3000
          hostPort      = 3000
        }
      ]
    }
  ])
}


# ALB

resource "aws_lb" "alb" {

  name = "tutedude-alb"

  load_balancer_type = "application"

  security_groups = [
    aws_security_group.ecs_sg.id
  ]

  subnets = [
    aws_subnet.public1.id,
    aws_subnet.public2.id
  ]
}

# TARGET GROUPS


resource "aws_lb_target_group" "frontend" {

  name = "frontend-tg"

  port = 3000

  protocol = "HTTP"

  vpc_id = aws_vpc.main.id

  target_type = "ip"
}

resource "aws_lb_target_group" "backend" {

  name = "backend-tg"

  port = 5000

  protocol = "HTTP"

  vpc_id = aws_vpc.main.id

  target_type = "ip"
}


# LISTENER


resource "aws_lb_listener" "frontend" {

  load_balancer_arn = aws_lb.alb.arn

  port = 80

  protocol = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}


# ECS SERVICES


resource "aws_ecs_service" "backend" {

  name = "backend-service"

  cluster = aws_ecs_cluster.main.id

  task_definition = aws_ecs_task_definition.backend.arn

  launch_type = "FARGATE"

  desired_count = 1

  network_configuration {

    assign_public_ip = true

    security_groups = [
      aws_security_group.ecs_sg.id
    ]

    subnets = [
      aws_subnet.public1.id,
      aws_subnet.public2.id
    ]
  }

}

resource "aws_ecs_service" "frontend" {

  name = "frontend-service"

  cluster = aws_ecs_cluster.main.id

  task_definition = aws_ecs_task_definition.frontend.arn

  launch_type = "FARGATE"

  desired_count = 1

  network_configuration {

    assign_public_ip = true

    security_groups = [
      aws_security_group.ecs_sg.id
    ]

    subnets = [
      aws_subnet.public1.id,
      aws_subnet.public2.id
    ]
  }

  load_balancer {

    target_group_arn = aws_lb_target_group.frontend.arn

    container_name = "frontend"

    container_port = 3000
  }

  depends_on = [
    aws_lb_listener.frontend
  ]
}

