-- Tạo database nếu chưa có
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'MovieDB')
BEGIN
    CREATE DATABASE MovieDB;
END
GO

USE MovieDB;
GO

-- Xóa bảng nếu đã tồn tại
IF OBJECT_ID('dbo.MovieSchedule', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.MovieSchedule;
END
GO

-- Tạo bảng MovieSchedule
CREATE TABLE dbo.MovieSchedule (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Theater NVARCHAR(255) NOT NULL,
    NameMovie NVARCHAR(255) NOT NULL,
    [Day] TINYINT NOT NULL,
    [Month] TINYINT NOT NULL,
    [Time] TIME NOT NULL
);
GO
