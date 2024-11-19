data "aws_availability_zones" "available" {}

resource "aws_vpc" "web_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "web_vpc"
  }
}

resource "aws_subnet" "web_subnet" {
  count             = 3
  vpc_id            = aws_vpc.web_vpc.id
  cidr_block        = var.subnet_cidr[count.index]
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "web_subnet_${count.index}"
  }
}

resource "aws_internet_gateway" "web_igw" {
  vpc_id = aws_vpc.web_vpc.id
  tags = {
    Name = "web_igw"
  }
}

resource "aws_route_table" "web_rt" {
  vpc_id = aws_vpc.web_vpc.id
  tags = {
    Name = "web_rt"
  }
}

resource "aws_route" "web_route" {
  route_table_id         = aws_route_table.web_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.web_igw.id
}

resource "aws_route_table_association" "web_rta" {
  count          = 3
  subnet_id      = aws_subnet.web_subnet[count.index].id
  route_table_id = aws_route_table.web_rt.id
}
